# Core Python
from datetime import datetime, timedelta

from authentication.models import Patient, Practitioner
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
# Django Functions
from django.shortcuts import render, redirect
from .forms import EditAccount, AddPatient, AddReading, AddPractitioner, CompleteDelivery
from django.utils import timezone

import pytz

# Labor Tracker
from .models import PartoMeasure, Partograph
from .choices import DELIVERY_TYPES


# Login Required to access
@login_required(login_url="/auth/login/", redirect_field_name=None)
def portal_home(request):
    return render(request, "portal_home.html", context={'staff': request.user.get_username})


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def add_patient(request):
    form = AddPatient(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/patient-list')
    context = {
        "form": form,
        "usertype": 'Patient'
    }
    return render(request, "add_user.html", context)


@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def add_practitioner(request):
    form = AddPractitioner(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/patient-list')
    context = {
        "form": form,
        "usertype": 'Practitioner'
    }
    return render(request, "add_user.html", context)


@login_required(login_url="/auth/login/", redirect_field_name=None)
def portal_account(request):
    user = request.user
    form = EditAccount(request.POST or None, instance=user,
                       initial={
                           'username': user.username,
                           'email': user.email,
                           'first_name': user.first_name,
                           'last_name': user.last_name,
                           'password': user.password
                       })

    if request.method == 'POST' and form.is_valid():
        form.save()

    context = {
        "form": form
    }

    # TODO : Show List View of Account Information
    return render(request, "account.html", context)

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def add_partograph(request):
    try:
        patient_id = request.session['patient_id']
    except KeyError:
        return redirect('/patient-list')
    request.session['patient_id'] = None
    patient = Patient.objects.get(pk=patient_id)
    if patient_id is not None:
        partograph = Partograph(patient=patient, provider=patient.practitioner)
        partograph.save()
        return redirect('/partograph/{}'.format(partograph.id))
    else:
        return redirect('/patient-list')


@login_required(login_url="/auth/login/", redirect_field_name=None)
def partograph(request, partograph_id=0):
    partograph = Partograph.objects.get(pk=partograph_id)
    patient = Patient.objects.get(pk=partograph.patient.id)

    context = {
        'patient': patient,
        'partograph': partograph,
    }

    measures = get_measures(partograph)
    dystocia, m = partograph.get_dystocia_points()
    context = {
        'patient': patient,
        'partograph': partograph,
        'dystocia': dystocia,
        'maxHours': max(node['x'] for node in dystocia),
        'minHours': -m,
        'dilation': measures['dilation'],
        #'descent': measures['descent'],
        'status': get_status(partograph, dystocia)
    }
    if not partograph.active:
        context['status'] = 'Complete'
    request.session['partograph_id'] = partograph.id
    return render(request, "partograph.html", context)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def add_reading(request):
    form = AddReading(request.POST)
    try:
        partograph_id = request.session['partograph_id']
    except KeyError:
        return redirect('/patient-list')
    if request.method == 'POST' and form.is_valid():
        measure = PartoMeasure()
        try:
            partograph = Partograph.objects.get(pk=partograph_id)
        except ObjectDoesNotExist as e:
            print("Error: {}, {}".format(e.args, partograph_id))
            return redirect('/add-reading')
        all_measures = partograph.partomeasure_set.all()

        update_time = timezone.make_aware(datetime.combine(form.cleaned_data['date_taken'], form.cleaned_data['time_taken']))
        measure.time_taken = update_time
        #time_hr = form.cleaned_data['time_hr']
       
        measure.dilation_cm = form.cleaned_data['dilation_cm']
        if all_measures and measure.dilation_cm >= 5:
            if not partograph.labor_start:
                partograph.labor_start = measure.time_taken
            measure.time_since_active_labor = measure.time_taken - partograph.labor_start
            # no measurements are recorded until we measure at least 5 cm?
            measure.partograph = partograph
            measure.save()
        return redirect('/partograph/{}'.format(partograph.id))

        # this method uses the hours since labor start input instead of time input
        #else:
        #    first_measure = all_measures[0]
        #    if time_hr is None:
        #        measure.time_since_active_labor = measure.time_taken - partograph.labor_start
        #    else:
        #        measure.time_since_active_labor = timedelta(hours=time_hr)  # To sec
        #        measure.time_taken = first_measure.time_taken + measure.time_since_active_labor
        #        print("Time hr = {}, time_taken = {}".format(time_hr, measure.time_taken))
        #measure.time_since_active_labor = timedelta(first_measure.time_taken, timedelta(0, form.cleaned_data['time_hr']*3600)+first_measure.time_taken)
        #measure.descent = form.cleaned_data['descent']
        #measure.station = form.cleaned_data['station']

    elif request.method == 'POST' and not form.is_valid():
        return render(request, 'add_reading.html', context={"form": form})
    return render(request, 'add_reading.html', context={"form": AddReading()})


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def complete_delivery(request):
    form = CompleteDelivery(request.POST)
    context = dict()
    try:
        partograph_id = request.session['partograph_id']
    except KeyError:
        return redirect('/patient-list')
    partograph = Partograph.objects.get(pk=partograph_id)
    context['patient'] = partograph.patient
    if request.method == 'POST' and form.is_valid():
        print(form.cleaned_data['delivery_type'])

        partograph.active = False
        partograph.live_birth = form.cleaned_data['live_birth']
        partograph.delivery_type = form.cleaned_data['delivery_type']
        partograph.newborn_weight_lbs = form.cleaned_data['newborn_weight_lbs']
        partograph.newborn_weight_oz = form.cleaned_data['newborn_weight_oz']
        partograph.delivery_time = timezone.make_aware(datetime.combine(form.cleaned_data['delivery_date'],
                                              form.cleaned_data['delivery_time']))
        partograph.save()

        patient = partograph.patient  # TODO update patient fields
        if partograph.delivery_type == 1:
            patient.vaginal_births += 1
        patient.save()
        request.session['partograph_id'] = None
        request.session['patient_id'] = None
        return redirect('/patient/{}'.format(patient.id))
    elif request.method == 'POST' and not form.is_valid():
        context['form'] = form
        return render(request, 'complete_delivery.html', context=context)

    context['form'] = CompleteDelivery(initial={
        'delivery_time': timezone.now(),  # TODO Timezone snafu - will likely want to read user's preferred TZ
        'delivery_date': timezone.now()
    })

    return render(request, 'complete_delivery.html', context=context)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def patient_list(request):
    request.session['patient_id'] = None
    context = {
        'patients': Patient.objects.all()
    }
    return render(request, "patient/patient_list.html", context)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def patient_view(request, id=0):
    patient = Patient.objects.get(pk=id)
    all_partographs = Partograph.objects.filter(patient_id=id).order_by('-id')
    request.session['patient_id'] = id
    if len(Partograph.objects.filter(patient_id=id).filter(active=True)) > 0:
        in_labor = True
    else:
        in_labor = False
    context = {
        'patient': patient,
        'partographs': all_partographs,
        'in_labor': in_labor
    }

    return render(request, "patient/patient_view.html", context)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def current_labors(request):
    partographs = Partograph.objects.filter(active=True)
    latest_measures = dict()
    for partograph in partographs:
        try:
            latest_measures[partograph.id] = partograph.partomeasure_set.all().order_by('-time_taken')[0]
        except IndexError:
            continue

    context = {
        'partographs': partographs,
        'dilations': dict(),
        'descents': dict(),
        'risks': dict()
    }

    for p_id, measure in latest_measures.items():
        context['dilations'][p_id] = measure.dilation_cm
        context['descents'][p_id] = measure.descent
        # TODO status determination

    return render(request, "current_labors.html", context)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/auth/login/", redirect_field_name=None)
def practitioner_list(request):
    practitioners = Practitioner.objects.all()
    context = {
        'practitioners': practitioners
    }
    return render(request, "practitioner_list.html", context)


def page_not_found(request):
    return render(request, "404.html")


def get_status(partograph, dystocia):
    measures = partograph.partomeasure_set.all().filter(dilation_cm__gte=4)
    if measures.count() == 0:
        return 'Early Labor'
    else:
        m = measures.order_by('-time_taken').first()
        for d in dystocia:
            if d['y'] == m.dilation_cm:
                hoursSinceStart = m.time_since_active_labor.seconds / 3600
                if hoursSinceStart >= d['x']: # in the red
                    return 'Slow Labor'
                break
        return 'On Track'


def get_measures(partograph):
    measures = partograph.partomeasure_set.all().order_by('time_taken')
    data = {
        'descent': [],
        'dilation': [],
        'times': []
    }
    if len(measures) > 0:
        m = measures[0]
        onset = m.time_taken
        data['descent'].append({'x': 0, 'y': m.descent})
        data['dilation'].append({'x': 0, 'y': m.dilation_cm})
        data['times'].append(0)
    for m in measures[1:]:
        delta = m.time_taken - onset
        delta = delta.seconds / 3600
        data['descent'].append({'x': delta, 'y': m.descent})
        data['dilation'].append({'x': delta, 'y': m.dilation_cm})
        data['times'].append(m.time_taken)
    return data


# MOCK FUNCTIONS
def get_mock_measurements(partograph):
    measures = [
        PartoMeasure(partograph=partograph, dilation_cm=4, descent=-3, time_taken=datetime(2008, 1, 1, 21)),
        PartoMeasure(partograph=partograph, dilation_cm=4.2, descent=-3, time_taken=datetime(2018, 1, 1, 22)),
        PartoMeasure(partograph=partograph, dilation_cm=4.4, descent=-1, time_taken=datetime(2018, 1, 1, 23)),
        PartoMeasure(partograph=partograph, dilation_cm=5.2, descent=-0, time_taken=datetime(2018, 1, 1, 0))
    ]
    data = {
        'descent': [],
        'dilation': [],
        'times': []
    }
    hour = 0
    for m in measures:
        data['descent'].append({'x': hour, 'y': m.descent})
        data['dilation'].append({'x': hour, 'y': m.dilation_cm})
        hour += 1
    return data


def get_mock_patient():
    return Patient(
        name="Louise Parker",
        age=21,
        height=63,
        weight=125
    )

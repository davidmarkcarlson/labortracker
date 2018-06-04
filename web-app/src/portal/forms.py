import datetime as dt
from authentication.models import User, Patient, Practitioner
from django.forms import ModelForm, CharField, IntegerField, TextInput, ChoiceField, ModelChoiceField, Form, \
    HiddenInput, DateTimeField, TimeField, DateField, BooleanField
from django.forms.widgets import Select, DateTimeInput, TimeInput, DateInput, SelectDateWidget
from .choices import DELIVERY_TYPES
from django import forms
from django.utils import timezone


class EditAccount(ModelForm):
    username = CharField(label='Username', widget=TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    email = CharField(label='Email Address', widget=TextInput(attrs={'class': 'form-control'}))
    first_name = CharField(label='First Name', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = CharField(label='Last Name', widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(EditAccount, self).__init__(*args, **kwargs)

class AddPatient(ModelForm):
    name = CharField(label='Name', required=True, widget=TextInput(attrs={'class': 'form-control'}))
    height = IntegerField(label='Height (in.)', required=True, widget=TextInput(attrs={'class': 'form-control'}))
    weight = IntegerField(label='Weight (lbs)', required=True, widget=TextInput(attrs={'class': 'form-control'}))
    age = IntegerField(label='Age', required=True, widget=TextInput(attrs={'class': 'form-control'}))
    gravida = IntegerField(label='Gravidity', required=False, widget=TextInput(attrs={'class': 'form-control'}))
    para = IntegerField(label='Parity', required=False, widget=TextInput(attrs={'class': 'form-control'}))
    vaginal_births = ChoiceField(choices=[(x, x) for x in range(0, 70)], label = 'Vaginal Births')
    practitioner = ModelChoiceField(required=True, queryset=Practitioner.objects)

    class Meta:
        model = Patient
        fields = ['name', 'height', 'weight', 'age','gravida', 'para','vaginal_births', 'practitioner']

    def __init__(self, *args, **kwargs):
        super(AddPatient, self).__init__(*args, **kwargs)

class CreatePartograph(ModelForm):
    pass

class AddReading(Form):
    partograph = IntegerField(widget=HiddenInput(), required=False)
    dilation_cm = IntegerField(label='Dilation (cm)', required=True, widget=TextInput(attrs={'class': 'form-control'}),
                               min_value=4, max_value=10)
    descent = IntegerField(label='Descent', required=True, widget=TextInput(attrs={'class': 'form-control'}),
                           min_value=-3, max_value=3)
    date_taken = DateField(required=True, initial=timezone.now(), widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time_taken = TimeField(required=True, initial=timezone.now(), widget=TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    time_hr = IntegerField(label='Hour', required=False, widget=TextInput(attrs={'class': 'form-control'}), min_value=0,
                           max_value=24)
    station = CharField(label='Station', required=True, widget=TextInput(attrs={'class': 'form-control'}))

    #def clean_time_taken(self):
    #    data = self.cleaned_data['time_taken']
    #    if data > timezone.now().time():
    #        raise forms.ValidationError("Cannot add a reading in the future")
    #    return data

    #def clean_date_taken(self):
    #    data = self.cleaned_data['date_taken']
    #    if data > timezone.now().date():
    #        raise forms.ValidationError("Cannot add a reading in the future")
    #    return data

class CompleteDelivery(Form):
    delivery_date = DateField(required=True, initial=timezone.now(), widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    delivery_time = TimeField(required=True, initial=timezone.now(), widget=TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    delivery_type = ChoiceField(required=True, choices=DELIVERY_TYPES, widget=Select(attrs={'class': 'form-control'}))
    newborn_weight_lbs = IntegerField(min_value=0, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    newborn_weight_oz = IntegerField(min_value=0, max_value=16, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    live_birth = BooleanField(required=False)

    def clean_delivery_date(self):
        data = self.cleaned_data['delivery_date']
        if data > timezone.now().date():
            raise forms.ValidationError("Cannot set delivery date in the future")
        return data

    def clean_delivery_time(self):
        data = self.cleaned_data['delivery_time']
        if data > timezone.now().time():
            raise forms.ValidationError("Cannot set delivery time in the future")
        return data

class AddPractitioner(ModelForm):
    title = CharField(label='Title', required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Practitioner
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(AddPractitioner, self).__init__(*args, **kwargs)

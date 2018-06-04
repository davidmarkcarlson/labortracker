from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect

def loginpage(request):
    context = {
        "title": "Login",
        "form_title": 'Login'
    }
    response = auth_views.login(request, template_name='login.html', extra_context=context)
    return response


def forgot(request):
    context = {
        "title": "Account Recovery",
        "form_title": 'Account Recovery'
    }
    return render(request, 'forgot-user.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    context = {
        "title": "Signup",
        "form_title": 'Signup',
        "form": form
    }
    return render(request, 'signup.html', context)

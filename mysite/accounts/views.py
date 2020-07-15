from . import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        create_user_if_form_is_valid(form)
    else:
        form = forms.CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', context={'form': form})

def create_user_if_form_is_valid(form):
    if form.is_valid():
        # Should check beforehand if the user already exists.
        user = get_user_model().objects.create_user(
            username = form.cleaned_data['email'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password1']
        )
        # Later could add e-mail functionality for verification of e-mail

def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        user = authetnicate_user(form)

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('movies:favorite'))
        # Should otherwise add a message in the context that login failed.
    else:
        form = forms.LoginForm()

    return render(request, 'accounts/login.html', context={'form': form})

def authetnicate_user(form):
    user = None

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)

    return user

def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('movies:index'))

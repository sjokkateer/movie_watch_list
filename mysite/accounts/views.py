from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Should move forms to separate file
input_attributes = {'class': 'input'}

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs=input_attributes))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=input_attributes))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=input_attributes))
    
    class Meta:
        model = get_user_model()
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs=input_attributes))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=input_attributes))


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # could factor out a method to create_user_if_form_is_valid
        if form.is_valid():
            # Should check beforehand if the user already exists.
            user = get_user_model().objects.create_user(
                username = form.cleaned_data['email'],
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password1']
            )
            # Later could add e-mail functionality for verification of e-mail
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', context={'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Could factor out a method to something along the line of authenticate user with form as argument
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)

                return HttpResponseRedirect(reverse('movies:favorite'))
            
            # Should add something when login failed (ultimately)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', context={'form': form})

def logout_view(request):
    logout(request)

    return HttpResponseRedirect(reverse('movies:index'))

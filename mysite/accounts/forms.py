from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views import View

input_attributes = {'class': 'input'}
password_attributes = {'autocomplete': 'new-password', 'class': 'input'}

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=password_attributes))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=password_attributes))
    
    class Meta:
        model = get_user_model()
        # Fields generated from the model automatically
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs=input_attributes),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs=input_attributes))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=input_attributes))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1')

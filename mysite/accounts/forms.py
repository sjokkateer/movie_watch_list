from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


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

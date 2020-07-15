from django import forms
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'input'}))
    
    class Meta:
        model = get_user_model()
        fields = ('email',)


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

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

def login(request):
    return 'Bla'
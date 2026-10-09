from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'conform password'}))
    class Meta:
        model = User
        fields=['username','email','password']
        widgets = {
            'username':forms.TextInput(
                attrs={'placeholder':'enter username'}
            ),
            'email':forms.EmailInput(
                attrs={'placeholder':'enter email'}
            ),
        }
class LoginForm(forms.ModelForm):
    class Meta:
        model= User
        fields=['username','password']
        widgets={
            'username':forms.TextInput(
                attrs={'placeholder':'enter username'}
            ),
            'password':forms.PasswordInput(
                attrs={'placeholder':"enter password"}
            )
        }
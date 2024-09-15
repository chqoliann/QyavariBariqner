from django import forms
from django.contrib.auth.models import User


class ManagerLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
        
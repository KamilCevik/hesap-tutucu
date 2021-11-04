from django import forms
from django.contrib.auth.models import User
from django.forms import fields


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)

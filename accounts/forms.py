from django import forms
from django.contrib.auth.models import User


class ChangePassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                    'type': 'password',
                                                    'placeholder': '********',
                                                    'required': '',
                                                    'id': 'password',
                                                    'align': 'right'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                    'type': 'new-password',
                                                    'placeholder': '********',
                                                    'required': '',
                                                    'id': 'new_password',
                                                    'align': 'right'}))

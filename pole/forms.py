from django import forms
from .models import *
from django.contrib.auth.models import User


class NumeroForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['telephone']



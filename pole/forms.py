from django import forms
from .models import *
from django.contrib.auth.models import User


class NumeroForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['telephone']
        widgets = {'telephone': forms.TextInput(attrs={'placeholder': '06XXXXXXXX'})}


class UserForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'DDN', 'telephone', 'pf', 'ph']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Parker'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Tony'}),
            'DDN': forms.TextInput(attrs={'placeholder': '17/05/1982'}),
            'telephone': forms.TextInput(attrs={'placeholder': '06XXXXXXXX'})}


class AjoutBilletForm(forms.ModelForm):
    class Meta:
        model = Billet
        fields = ['personne', 'billet']


class PrepaForm(forms.ModelForm):
    class Meta:
        model = Camille
        fields = ['joueuse', 'exercice', 'plaisir', 'effort']

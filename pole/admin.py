from django.contrib import admin
from .models import *


class PersonneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'gare']


admin.site.register(Personne, PersonneAdmin)

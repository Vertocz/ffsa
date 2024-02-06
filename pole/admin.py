from django.contrib import admin
from .models import *


class PersonneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'gare']

class EntreeAdmin(admin.ModelAdmin):
    list_display = ['mot']


admin.site.register(Personne, PersonneAdmin)
admin.site.register(Entree, EntreeAdmin)

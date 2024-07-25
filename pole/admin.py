from django.contrib import admin
from .models import *


class PersonneAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'telephone', 'pf', 'ph']


class BilletAdmin(admin.ModelAdmin):
    list_display = ['personne', 'billet']


class EntreeAdmin(admin.ModelAdmin):
    list_display = ['mot']


class GifAdmin(admin.ModelAdmin):
    list_display = ['mot', 'image']


class CamilleAdmin(admin.ModelAdmin):
    list_display = ['joueuse', 'jour', 'exercice', 'plaisir', 'effort']


admin.site.register(Personne, PersonneAdmin)
admin.site.register(Billet, BilletAdmin)
admin.site.register(Entree, EntreeAdmin)
admin.site.register(Gif, GifAdmin)
admin.site.register(Camille, CamilleAdmin)

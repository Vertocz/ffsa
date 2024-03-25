from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import auth, admin
from pole.views import *

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('membre/<int:id>/', personne, name='personne'),
    path('membre/<int:id>/billets/', billets, name="billets"),
    path('telecharger/billets/<str:billet>/', telecharger_billet, name='telecharger-billet'),
    path('telecharger/cartes/<str:carte>/', telecharger_carte, name='telecharger-carte'),
    path('dico/', dico, name='dico'),
    path('dico/<str:entree>/', mot, name='entree'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

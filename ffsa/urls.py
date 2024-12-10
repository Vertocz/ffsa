from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import auth, admin
from pole.views import *

urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('utilisateur/ajouter/', ajouter_utilisateur, name='ajouter-utilisateur'),
    path('utilisateur/<int:id>/', personne, name='personne'),
    path('utilisateur/<int:id>/billets/', billets, name="billets"),
    path('telecharger/billets/<str:billet>/', telecharger_billet, name='telecharger-billet'),
    path('telecharger/cartes/<str:carte>/', telecharger_carte, name='telecharger-carte'),
    path('dico/', dico, name='dico'),
    path('dico/<str:entree>/', mot, name='entree'),
    path('billets/', ajouter_billet, name='ajouter-billet'),
    path('quiz/', quiz, name='quiz'),
    path('quiz/reponses', quiz, name='reponses'),
    path('menu/', menu, name='menu'),
    path('prepa/', prepa_camille, name='prepa'),
    path('camille/', camille, name='camille'),
    path('entretien/', entretien_ete, name='entretien'),
    path('summerbody/', summer_bodies, name='summer'),
    path('summerbody/<int:id>/', summer_body, name='summer-indiv'),
    path('control/', control_view, name='control'),
    path('display/', display_view, name='display'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

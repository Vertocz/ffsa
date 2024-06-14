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
    path('timer/', timer, name='timer'),
    path('menu/', menu, name='menu')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

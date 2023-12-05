import glob
import mimetypes
import os
from pathlib import Path
from urllib import response

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, FileResponse, Http404, HttpResponseRedirect
from unidecode import unidecode
from django.shortcuts import render, redirect
from django.contrib import messages
from pole.models import *
from .forms import NumeroForm


def index(request):
    if request.method == 'POST':
        form = NumeroForm(request.POST)
        numero = form.data['telephone']
        try:
            personne = Personne.objects.get(telephone=numero)
            return billets(request, personne)

        except ObjectDoesNotExist:
            form = NumeroForm()

    else:
        form = NumeroForm()

    return render(request, "index.html", {"form": form, "billets": billets})


def billets(request, personne):
    billets = []
    carte = ''
    nom = str(unidecode(personne.nom).upper())
    characters = "'!? "

    for x in range(len(characters)):
        nom = nom.replace(characters[x], "")
    BASE_DIR = Path(__file__).resolve().parent.parent
    dossier_billets = BASE_DIR / 'pole/billets/'
    dossier_cartes = BASE_DIR / 'pole/cartes/'

    for root, dirs, files in os.walk(dossier_billets):
        for file in files:
            if nom in str(file):
                billets.append(str(file))

    for root, dirs, files in os.walk(dossier_cartes):
        for file in files:
            if nom in str(file):
                carte = str(file)

    return render(request, "billets.html", {'personne': personne, 'billets': billets, 'carte': carte, 'doss_billets': dossier_billets, 'doss_cartes': dossier_cartes})


def telecharger_billet(file):
    BASE_DIR = Path(__file__).resolve().parent.parent
    root = BASE_DIR / 'pole/billets/'
    return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))


def telecharger_carte(file):
    BASE_DIR = Path(__file__).resolve().parent.parent
    root = BASE_DIR / 'pole/cartes/'
    return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


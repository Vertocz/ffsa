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
        BASE_DIR = Path(__file__).resolve().parent.parent
        form = NumeroForm(request.POST)
        numero = form.data['telephone']
        try:
            personne = Personne.objects.get(telephone=numero)
            nom = str(unidecode(personne.nom).upper())
            characters = "'!? "
            for x in range(len(characters)):
                nom = nom.replace(characters[x], "")
            if 'carta' in request.POST:
                dossier_cartes = BASE_DIR / 'pole/cartes/'
                for root, dirs, files in os.walk(dossier_cartes):
                    print(root)
                    for file in files:
                        if nom in str(file):
                            return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))
            else:
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

    for root, dirs, files in os.walk(dossier_billets):
        for file in files:
            if nom in str(file):
                billets.append(str(file))

    if request.GET:
        print(request.GET)
        for x in range(len(billets)):
            for key in request.GET:
                if int(x) == int(key):
                    print("yes", x)
                    for root, dirs, files in os.walk(dossier_billets):
                        for file in files:
                            if str(file) == str(billets[x]):
                                return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))
                else:
                    print('no', key, x)

    return render(request, "billets.html", {'personne': personne, 'billets': billets, 'carte': carte, 'doss_billets': dossier_billets})


def telecharger_billet(personne, numero):
    BASE_DIR = Path(__file__).resolve().parent.parent
    root = BASE_DIR / 'pole/billets/'
    billets = []
    for root, dirs, files in os.walk(root):
        for file in files:
            if str(personne.nom) in str(file):
                billets.append(str(file))
    return FileResponse(open(str(os.path.join(root, billets[numero])), 'rb'), as_attachment=True, filename=str(billets[numero]))


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


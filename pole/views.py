import os
import re
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from unidecode import unidecode
from django.shortcuts import render, redirect
from django.contrib import messages
from ffsa.settings import MEDIA_ROOT
from pole.models import *
from .forms import NumeroForm


def index(request):
    if request.method == 'POST':
        form = NumeroForm(request.POST)
        phone = form.data['telephone'].replace(" ", "")
        numero = re.sub('\++33', '0', phone)


        try:
            personne = Personne.objects.get(telephone=numero)
            nom = str(unidecode(personne.nom).upper())
            characters = "'!? "
            for x in range(len(characters)):
                nom = nom.replace(characters[x], "")

            if 'carta' in request.POST:
                liste_cartes = []
                for root, dirs, files in os.walk(Path(MEDIA_ROOT).resolve() / 'cartes/'):
                    for file in files:
                        if nom in str(file):
                            liste_cartes.append(str(file))
                    if len(liste_cartes) == 0:
                        messages.success(request, ("Il n\'y a pas de carte disponible pour ce numéro"))
                        return redirect('index')
                    return cartes(request, personne, liste_cartes)

            if 'billetos' in request.POST:
                liste_billets = []
                for root, dirs, files in os.walk(Path(MEDIA_ROOT).resolve() / 'billets/'):
                    for file in files:
                        if nom in str(file):
                            liste_billets.append(str(file))
                return billets(request, personne, liste_billets)

        except ObjectDoesNotExist:
            form = NumeroForm()

    else:
        form = NumeroForm()

    return render(request, "index.html", {"form": form})


def billets(request, personne, liste_billets):
    return render(request, "billets.html", {'personne': personne, "billets": liste_billets})


def cartes(request, personne, liste_cartes):
    return render(request, "cartes.html", {'personne': personne, "cartes": liste_cartes})


def telecharger_billet(request, billet):
    return FileResponse(open(Path(MEDIA_ROOT).resolve() / 'billets' / billet, 'rb'), as_attachment=True)


def telecharger_carte(request, carte):
    return FileResponse(open(Path(MEDIA_ROOT).resolve() / 'cartes' / carte, 'rb'), as_attachment=True)


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


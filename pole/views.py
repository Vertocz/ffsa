import os
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
        numero = form.data['telephone']
        try:
            personne = Personne.objects.get(telephone=numero)
            nom = str(unidecode(personne.nom).upper())
            characters = "'!? "
            for x in range(len(characters)):
                nom = nom.replace(characters[x], "")

            if 'carta' in request.POST:
                for root, dirs, files in os.walk(Path(MEDIA_ROOT).resolve() / 'cartes/'):
                    for file in files:
                        if nom in str(file):
                            return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))
                        else:
                            messages.success(request, ("Il n\'y a pas de carte disponible pour ce numéro"))
                            return redirect('index')

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


def telecharger_billet(request, billet):
    return FileResponse(open(Path(MEDIA_ROOT).resolve() / 'billets' / billet, 'rb'), as_attachment=True)


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


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
            nom = str(unidecode(personne.nom).upper())
            characters = "'!? "

            for x in range(len(characters)):
                nom = nom.replace(characters[x], "")

        except ObjectDoesNotExist:
            nom = 'xxx'

        BASE_DIR = Path(__file__).resolve().parent.parent
        directory = BASE_DIR / 'pole/billets/'

        for root, dirs, files in os.walk(directory):
            for file in files:
                if nom in str(file):
                    return FileResponse(open(str(os.path.join(root, file)), 'rb'), as_attachment=True, filename=str(file))
                else:
                    form = NumeroForm()

    else:
        form = NumeroForm()

    return render(request, "index.html", {"form": form})


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


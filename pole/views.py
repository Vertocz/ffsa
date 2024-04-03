import os
import random
import re
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseRedirect
from unidecode import unidecode
from django.shortcuts import render, redirect
from django.contrib import messages
from ffsa.settings import MEDIA_ROOT
from pole.models import *
from .forms import NumeroForm, AjoutBilletForm


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
                for billet in Billet.objects.filter(personne=personne):
                    liste_billets.append(os.path.basename(billet.billet.file.name))
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


def ajouter_billet(request):
    if request.method == 'POST':
        form = AjoutBilletForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le billet a bien été mis en ligne')
            return render(request, "ajout_billets.html", {"form": form})
        else:
            messages.success(request, 'Quelque chose ne s\'est pas passé correctement')
            form = AjoutBilletForm()
            return render(request, "ajout_billets.html", {'form': form})

    else:
        form = AjoutBilletForm()
        return render(request, "ajout_billets.html", {'form': form})


def telecharger_billet(request, billet):
    return FileResponse(open(Path(MEDIA_ROOT).resolve() / 'billets' / billet, 'rb'), as_attachment=True)


def telecharger_carte(request, carte):
    return FileResponse(open(Path(MEDIA_ROOT).resolve() / 'cartes' / carte, 'rb'), as_attachment=True)


def personne(request, id):
    fiche = Personne.objects.get(id=id)
    return render(request, "personne.html", {'personne': fiche})


def dico(request):
    entrees = Entree.objects.all().order_by('mot')
    return render(request, "dico.html", {'entrees': entrees})


def quiz(request):
    entrees = Entree.objects.all()
    questions = []
    for entree in entrees:
        if len(Gif.objects.filter(mot=entree)) > 0:
            video = random.choices(Gif.objects.filter(mot=entree))
            pas_video = False
        else:
            video = entree.definition
            pas_video = True
        propositions = []
        reponse = entree.mot
        propositions.append(reponse)
        while len(propositions) < 3:
            for fausse_reponse in random.choices(entrees, k=1):
                if fausse_reponse.mot in propositions:
                    pass
                else:
                    propositions.append(fausse_reponse.mot)
        random.shuffle(propositions)
        questions.append([propositions, video, pas_video])

    if request.method == 'POST':
        print(request.POST.getlist('quiz'))
        score = 0
        reponses_utilisateur = request.POST.getlist('quiz')
        for question, reponse_utilisateur in zip(questions, reponses_utilisateur):
            print(question[0][0])
            reponse_correcte = question[0][0]
            if reponse_utilisateur == reponse_correcte:
                score += 1
            else:
                pass
        return render(request, "reponses.html", {'questions': questions, 'score': score})

    else:
        random.shuffle(questions)
        return render(request, "quiz.html", {'questions': questions})


def mot(request, entree):
    entree_en_cours = Entree.objects.get(mot=entree)
    videos = Gif.objects.filter(mot=entree_en_cours)
    return render(request, 'mot.html', {'entree': entree_en_cours, 'gifs': videos})

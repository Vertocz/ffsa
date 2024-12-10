import datetime
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
from .forms import *


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


def menu(request):
    return render(request, 'menu.html')


def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'L\'utilisateur a bien été ajouté')
            return render(request, "ajout_utilisateur.html", {"form": form})
        else:
            messages.success(request, 'Quelque chose ne s\'est pas passé correctement')
            form = UserForm()
            return render(request, "ajout_utilisateur.html", {'form': form})

    else:
        form = UserForm()
        return render(request, "ajout_utilisateur.html", {'form': form})


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
        propositions = []

        types_questions = ['mot', 'def']
        type_question = random.choice(types_questions)

        if len(Gif.objects.filter(mot=entree)) > 0:
            pas_video = False
        else:
            pas_video = True

        if type_question == 'mot':
            if pas_video is False:
                pas_video = True
            question = entree.mot
            reponse = entree.definition
            propositions.append(reponse)
            while len(propositions) < 3:
                for fausse_reponse in random.choices(entrees, k=1):
                    if fausse_reponse.definition in propositions:
                        pass
                    else:
                        propositions.append(fausse_reponse.definition)

        elif type_question == 'def':
            if pas_video is False:
                question = random.choices(Gif.objects.filter(mot=entree))
            else:
                question = entree.definition
            reponse = entree.mot
            propositions.append(reponse)
            while len(propositions) < 3:
                for fausse_reponse in random.choices(entrees, k=1):
                    if fausse_reponse.mot in propositions:
                        pass
                    else:
                        propositions.append(fausse_reponse.mot)

        random.shuffle(propositions)
        questions.append([propositions, question, pas_video, entree])

    if request.method == 'POST':
        score = 0
        correct = []
        incorrect = []
        for entree in entrees:
            if entree.mot == request.POST.get(entree.mot) or entree.definition == request.POST.get(entree.mot):
                correct.append(entree)
                score += 1
            else:
                incorrect.append(entree)

        return render(request, "reponses.html", {'incorrect': incorrect, 'score': score, 'gifs': Gif.objects.all(), 'entrees': len(entrees)})

    else:
        random.shuffle(questions)
        return render(request, "quiz.html", {'questions': questions})


def mot(request, entree):
    entree_en_cours = Entree.objects.get(mot=entree)
    videos = Gif.objects.filter(mot=entree_en_cours)
    return render(request, 'mot.html', {'entree': entree_en_cours, 'gifs': videos})


def prepa_camille(request):
    if request.method == 'POST':
        form = PrepaForm(request.POST)
        form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
        if form.is_valid():
            Camille(jour=datetime.datetime.today(), joueuse=Personne.objects.get(id=form.data['joueuse']), exercice=form.data['exercice'], plaisir=form.data['plaisir'], effort=form.data['effort']).save()
            messages.success(request, 'Le test a bien été rempli')
            return render(request, "prepa.html", {'form': form})
        else:
            messages.success(request, 'Quelque chose ne s\'est pas passé correctement')
            form = PrepaForm()
            form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
            return render(request, "prepa.html", {'form': form})
    else:
        form = PrepaForm()
        form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
        return render(request, "prepa.html", {'form': form})


def camille(request):
    tests = Camille.objects.all()
    return render(request, "camille.html", {'tests': tests})


def entretien_ete(request):
    if request.method == 'POST':
        form = Ete_exoForm(request.POST)
        form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
        if form.is_valid():
            Ete_exo(jour=form.data['jour'], joueuse=Personne.objects.get(id=form.data['joueuse']), exercice=form.data['exercice'], duree=form.data['duree']).save()
            messages.success(request, 'L\'exercice a bien été enregistré')
            resume_joueuse = Ete_exo.objects.filter(joueuse=Personne.objects.get(id=form.data['joueuse']))
            return render(request, "entretien_ete.html", {'form': form, 'resume': resume_joueuse, 'joueuse': Personne.objects.get(id=form.data['joueuse'])})
        else:
            print(form.errors.as_data())
            messages.success(request, 'Quelque chose ne s\'est pas passé correctement')
            form = Ete_exoForm()
            form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
            return render(request, "entretien_ete.html", {'form': form})
    else:
        form = Ete_exoForm()
        form.fields["joueuse"] = forms.ModelChoiceField(queryset=Personne.objects.filter(pf=True))
        return render(request, "entretien_ete.html", {'form': form})


def summer_bodies(request):
    resume = Ete_exo.objects.all().order_by('jour')
    return render(request, "summerbody.html", {'resume': resume})


def summer_body(request, id):
    resume = Ete_exo.objects.filter(joueuse=Personne.objects.get(id=id)).order_by('jour')
    return render(request, "summerbody.html", {'resume': resume})


def control_view(request):
    return render(request, 'control.html')


def display_view(request):
    return render(request, 'display.html')


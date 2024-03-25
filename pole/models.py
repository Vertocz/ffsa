from django.core.files.storage import FileSystemStorage
from django.db import models


class Personne(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    DDN = models.DateField('Date de Naissance', null=True, blank=True)
    gare = models.CharField(max_length=500, null=True, blank=True)
    carte = models.CharField(max_length=50, blank=True, null=True)
    fin_validite = models.DateField(blank=True, null=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    mail = models.EmailField(blank=True)
    pf = models.BooleanField(default=False)
    ph = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.prenom}'


class Entree(models.Model):
    mot = models.CharField(max_length=200, null=True)
    definition = models.CharField(max_length=600, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    video = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.mot}'


class Gif(models.Model):
    mot = models.ForeignKey(Entree, on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to="gifs/")

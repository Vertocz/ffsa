from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import RadioSelect


class Personne(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    DDN = models.DateField('Date de Naissance', null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    pf = models.BooleanField('Pôle Féminin', default=False)
    ph = models.BooleanField('Pôle Masculin', default=False)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f'{self.nom + " " + self.prenom}'


class Billet(models.Model):
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE, null=False)
    billet = models.FileField(upload_to="billets/")


class Entree(models.Model):
    mot = models.CharField(max_length=200, null=True)
    definition = models.CharField(max_length=600, null=True)
    video = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.mot}'


class Gif(models.Model):
    mot = models.ForeignKey(Entree, on_delete=models.CASCADE, null=False)
    image = models.FileField(upload_to="gifs/")


class Camille(models.Model):
    jour = models.DateField()
    exercice = models.CharField(max_length=30)
    joueuse = models.ForeignKey(Personne, on_delete=models.CASCADE, null=False)
    plaisir = models.IntegerField()
    effort = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])


class Ete_exo(models.Model):
    joueuse = models.ForeignKey(Personne, on_delete=models.CASCADE, null=False)
    jour = models.DateField()
    exercice = models.CharField(max_length=30)
    duree = models.CharField(max_length=50)

"""
Définition des models.

Utilisateurs, Match etc.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class UserFCC(models.Model):
    """Utilisateurs FCC."""

    idUserFCC = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    tel = models.CharField(max_length=10, null=True, blank=True)
    titulaire = models.BooleanField(default=False)
    inscrit = models.IntegerField(default=0)
    paiement = models.BooleanField(default=False)
    photo = models.ImageField(null=True, blank=True, upload_to='avatar/')
    has_voted = models.BooleanField(default=False)
    dtUpdate = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        """Description."""
        return self.user.username


class Match(models.Model):
    """Matchs."""

    id_match = models.AutoField(primary_key=True)
    dateMatch = models.DateField(auto_now=False, auto_now_add=False, null=True)
    ouverte = models.IntegerField(default=0)
    inscrits = models.IntegerField(default=0)
    session = models.ForeignKey('Session')
    scoreA = models.IntegerField(null=True, blank=True)
    scoreB = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """Description."""
        return str(self.id_match)


class Joker(models.Model):
    """Description d'un joker."""

    match = models.ForeignKey('Match')
    joker = models.CharField(max_length=20)
    userFCC = models.ForeignKey('UserFCC')

    def __str__(self):
        """Description."""
        return str(self.joker) + ", joker de " + self.userFCC.user.username


class Session(models.Model):
    """Session."""

    id_session = models.AutoField(primary_key=True)
    nombreMatchs = models.IntegerField(default=0)
    ouverte = models.BooleanField(default=False)
    vainqueur = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        """Description."""
        return str(self.id_session)


class Resultat(models.Model):
    """Resultats."""

    match = models.ForeignKey('Match')
    userFCC = models.ForeignKey('UserFCC')
    equipe = models.CharField(max_length=1, default="A")
    buts = models.IntegerField(default=0)
    somme_notes = models.IntegerField(default=0)
    moyenne_note = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        """Description."""
        return "User " + self.userFCC.user.username + ", Equipe " + self.equipe + ", Match " + str(self.match.dateMatch)


class Stat(models.Model):
    """Stat."""

    session = models.ForeignKey('Session')
    userFCC = models.ForeignKey('UserFCC')
    points = models.IntegerField(default=0)
    victoire = models.IntegerField(default=0)
    nul = models.IntegerField(default=0)
    defaite = models.IntegerField(default=0)
    buts = models.IntegerField(default=0)
    classement = models.IntegerField(null=True)
    classement_last = models.IntegerField(null=True)

    def __str__(self):
        """Description."""
        return "User " + self.userFCC.user.username + ", Session " + str(self.session.id_session)

    def __init__(self, *args, **kwargs):
        """Description."""
        super(Stat, self).__init__(*args, **kwargs)
        self.nb_matchs = self.victoire + self.nul + self.defaite
        moy = 0
        if self.points > 0 and self.nb_matchs > 0:
            moy = self.points / self.nb_matchs
        self.moyenne = round(moy, 1)


class Compo(models.Model):
    """Composition."""

    session = models.ForeignKey('Session')
    userFCC = models.ForeignKey('UserFCC')
    equipe = models.CharField(max_length=1, default="A")

    def __str__(self):
        """Description."""
        return "User " + self.userFCC.user.username + ", Session " + str(self.session.id_session) + ", Equipe " + self.equipe


class Award(models.Model):
    """Awards."""

    id_award = models.AutoField(primary_key=True)
    annee = models.IntegerField(default='2015')
    nom_award = models.CharField(max_length=100)

    def __str__(self):
        """Description."""
        return "Award " + self.nom_award + " " + str(self.annee)


class AwardVainqueur(models.Model):
    """Lauréat d'un award."""

    award = models.ForeignKey('Award')
    userFCC = models.ForeignKey('UserFCC')

    def __str__(self):
        """Description."""
        return "Award " + self.award.nom_award + " " + str(self.award.annee) + self.userFCC.user.username


class News(models.Model):
    """News."""

    userFCC = models.ForeignKey('UserFCC')
    titre = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Description."""
        return self.titre + " par " + self.userFCC.user.username


class NoteMatch(models.Model):
    """Note pour un match donné."""

    id_note = models.AutoField(primary_key=True)
    joueur = models.ForeignKey('UserFCC', related_name="Joueur")
    userFCC = models.ForeignKey('UserFCC', related_name="Votant")
    match = models.ForeignKey('Match')
    note = models.IntegerField(default='0')

    def __str__(self):
        """Description."""
        return self.joueur.user.username + self.note + " par " + self.userFCC.user.username

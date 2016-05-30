"""
Définition formulaires utilisés sur le site.

Connexion, Resultats etc.
"""

from django import forms
from fcc.models import Resultat, Match, UserFCC, News, Joker, Session
from django.contrib.auth.models import User


class ConnexionForm(forms.Form):
    """Connexion."""

    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class YearAwardsForm(forms.Form):
    """Sélection de l'année des awards."""

    YEAR_AWARDS = [('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ]
    year = forms.ChoiceField(choices=YEAR_AWARDS)


class SessionForm(forms.Form):
    """Sélection de l'année des awards."""

    LISTE_SESSION = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
         ]
    s = forms.ChoiceField(choices=LISTE_SESSION)


class JokerForm(forms.Form):
    """Ajout d'un joker dans la compo."""

    joker = forms.CharField(label="Joker", max_length=20)


class ResultatTeamAForm(forms.ModelForm):
    """Résultat d'un joueur de l'équipe A."""

    userFCC = forms.ModelChoiceField(queryset=UserFCC.objects.all(), label="Joueur")
    buts = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Resultat
            fields = ('userFCC', 'buts',)


class ResultatTeamBForm(forms.ModelForm):
    """Résultat d'un joueur de l'équipe B."""

    userFCC = forms.ModelChoiceField(queryset=UserFCC.objects.all(), label="Joueur")
    buts = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Resultat
            fields = ('userFCC', 'buts',)


class ResultatMatchForm(forms.ModelForm):
    """Score du match."""

    scoreA = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}), initial=0)
    scoreB = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Match
            fields = ('scoreA', 'scoreB',)


class UserForm(forms.ModelForm):
    """Edition du profil."""

    email = forms.EmailField(label="email")

    class Meta:
        # Provide an association between the ModelForm and a model
            model = User
            fields = ('email',)


class UserFCCForm(forms.ModelForm):
    """Edition du profil."""

    tel = forms.CharField(max_length=10, label="GSM", required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = UserFCC
            fields = ('tel', 'photo',)


class NewsForm(forms.ModelForm):
    """Ajout d'une news sur la page d'accueil."""

    titre = forms.CharField(max_length=100)
    message = forms.Textarea()

    class Meta:
        # Provide an association between the ModelForm and a model
            model = News
            fields = ('titre', 'message',)

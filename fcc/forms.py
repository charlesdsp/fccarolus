"""
Définition formulaires utilisés sur le site.

Connexion, Resultats etc.
"""

from django import forms
from fcc.models import Resultat, Match, UserFCC, News, Joker, Session, Award
from django.contrib.auth.models import User


class ConnexionForm(forms.Form):
    """Connexion."""

    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class YearAwardsForm(forms.Form):
    """Sélection de l'année des awards."""
    liste_awards = Award.objects.values('annee').order_by('annee')
    liste_num_year = []
    annee = []
    for award in liste_awards:
        if award['annee'] not in annee:
            annee.append(award['annee'])
            liste_num_year.append((award['annee'], (award['annee'])))
    year = forms.ChoiceField(choices=liste_num_year)


class SessionForm(forms.Form):
    """Sélection de l'année des awards."""
    liste_session = Session.objects.all()
    liste_num_session = []
    for session in liste_session:
        liste_num_session.append((session.id_session, session.id_session))
    liste_num_session.append(('Global', ('Global')))
    s = forms.ChoiceField(choices=liste_num_session)


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

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe")

    class Meta:
        # Provide an association between the ModelForm and a model
            model = User
            fields = ('email', 'password')


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
    message = forms.Textarea(attrs={'rows': 10, 'cols': 30})

    class Meta:
        # Provide an association between the ModelForm and a model
            model = News
            fields = ('titre', 'message',)

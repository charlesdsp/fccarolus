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


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email ou Login"), max_length=254)

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("Les mots de passe ne sont pas identiques."),
        }
    new_password1 = forms.CharField(label=("Nouveau mot de passe"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("Confirmation du mot de passe"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


class YearAwardsForm(forms.Form):
    """Sélection de l'année des awards."""

    liste_awards = Award.objects.values('annee').order_by('annee')
    liste_num_year = []
    annee = []
    for award in liste_awards:
        if award['annee'] not in annee:
            annee.append(award['annee'])
            liste_num_year.append((award['annee'], (award['annee'])))
    print(liste_num_year)
    year = forms.ChoiceField(choices=liste_num_year)

    def __init__(self, *args, **kwargs):
        super(YearAwardsForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;", })


class SessionForm(forms.Form):
    """Sélection de l'année des awards."""
    liste_session = Session.objects.all()
    liste_num_session = []
    for session in liste_session:
        liste_num_session.append((session.id_session, session.id_session))
    liste_num_session.append(('Global', ('Global')))
    s = forms.ChoiceField(choices=liste_num_session)

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.fields['s'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;", })


class JokerForm(forms.Form):
    """Ajout d'un joker dans la compo."""

    joker = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control input-sm',
        'required': True,
        'placeholder': "Joker",
        'style': "width: auto; display: inline;",
        }))


class ResultatTeamAForm(forms.ModelForm):
    """Résultat d'un joueur de l'équipe A."""

    userFCC = forms.ModelChoiceField(queryset=UserFCC.objects.all(), label="Joueur")
    buts = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Resultat
            fields = ('userFCC', 'buts',)

    def __init__(self, *args, **kwargs):
        super(ResultatTeamAForm, self).__init__(*args, **kwargs)
        self.fields['userFCC'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;"})
        self.fields['buts'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;"})


class ResultatTeamBForm(forms.ModelForm):
    """Résultat d'un joueur de l'équipe B."""

    userFCC = forms.ModelChoiceField(queryset=UserFCC.objects.all(), label="Joueur")
    buts = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2, 'class': 'form-control input-sm'}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Resultat
            fields = ('userFCC', 'buts',)

    def __init__(self, *args, **kwargs):
        super(ResultatTeamBForm, self).__init__(*args, **kwargs)
        self.fields['userFCC'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;"})
        self.fields['buts'].widget.attrs.update({'class': 'form-control input-sm', 'style': "width: auto; display: inline;"})


class ResultatMatchForm(forms.ModelForm):
    """Score du match."""

    scoreA = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2, 'class': 'form-control input-sm', 'style': "width: auto; display: inline;"}), initial=0)
    scoreB = forms.IntegerField(widget=forms.TextInput(attrs={'size': 2, 'class': 'form-control input-sm', 'style': "width: auto; display: inline;"}), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = Match
            fields = ('scoreA', 'scoreB',)

    def __init__(self, *args, **kwargs):
        super(ResultatMatchForm, self).__init__(*args, **kwargs)
        self.fields['scoreA'].widget.attrs.update({'class': 'form-control input-sm', })
        self.fields['scoreA'].widget.attrs.update({'class': 'form-control input-sm'})


class UserForm(forms.ModelForm):
    """Edition du profil."""

    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Mot de passe")

    class Meta:
        # Provide an association between the ModelForm and a model
            model = User
            fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control input-sm', })
        self.fields['password'].widget.attrs.update({'class': 'form-control input-sm'})


class UserFCCForm(forms.ModelForm):
    """Edition du profil."""

    tel = forms.CharField(max_length=10, label="GSM", required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
            model = UserFCC
            fields = ('tel', 'photo',)

    def __init__(self, *args, **kwargs):
        super(UserFCCForm, self).__init__(*args, **kwargs)
        self.fields['tel'].widget.attrs.update({'class': 'form-control input-sm', })


class NewsForm(forms.ModelForm):
    """Ajout d'une news sur la page d'accueil."""

    titre = forms.CharField(max_length=100)
    message = forms.Textarea(attrs={'rows': 10, 'cols': 30})

    class Meta:
        # Provide an association between the ModelForm and a model
            model = News
            fields = ('titre', 'message',)

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['titre'].widget.attrs.update({'class': 'form-control input-sm', 'required': True, })
        self.fields['message'].widget.attrs.update({'class': 'form-control input-sm', 'required': True, })

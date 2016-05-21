"""
Définition des pages du site.

home, inscrits etc.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from fcc.models import UserFCC, Session, Compo, Match, Resultat, Stat
from fcc.forms import ConnexionForm, ResultatTeamAForm, ResultatTeamBForm, ResultatMatchForm, UserForm, UserFCCForm
import operator


@login_required
def home(request):
    """Page d'accueil."""
    sessionActive = Session.objects.filter(ouverte=True)[0]
    listeInscrits = UserFCC.objects.filter(inscrit=1 or 2)
    listeAbsents = UserFCC.objects.filter(inscrit=3)
    nbInscrits = len(listeInscrits)
    nbAbsents = len(listeAbsents)
    prochainMatch = Match.objects.filter(ouverte=True)[0]
    return render(request, 'fcc/home.html', {'prochainMatch': prochainMatch, 'sessionActive': sessionActive, 'nbInscrits': nbInscrits, 'nbAbsents': nbAbsents})


@login_required
def user(request, id_user=None):
    """Page de profil."""
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        userFCC_form = UserFCCForm(data=request.POST)

        if user_form.is_valid() and userFCC_form.is_valid():
            u = request.user
            uFCC = UserFCC.objects.get(user=u)
            u.email = user_form.cleaned_data['email']
            u.save()
            uFCC.tel = userFCC_form.cleaned_data['tel']
            if 'photo' in request.FILES:
                uFCC.photo = request.FILES['photo']
            uFCC.save()
        else:
            print(user_form.errors, userFCC_form.errors)

    if id_user is None:
        u = request.user
        id_user = UserFCC.objects.get(user=u)
        user_form = UserForm(initial={'email': id_user.user.email})
        userFCC_form = UserFCCForm(initial={'tel': id_user.tel, 'photo': id_user.photo})
        return render(request, 'fcc/user.html', {'user': id_user, 'user_form': user_form, 'userFCC_form': userFCC_form})
    user = get_object_or_404(UserFCC, idUserFCC=id_user)
    return render(request, 'fcc/user.html', {'user': user})


@login_required
def compo(request):
    """Page de la compo du match."""
    sessionActive = Session.objects.filter(ouverte=True)[0]
    compoAdispo = Compo.objects.filter(session__id_session=sessionActive.id_session, equipe='A', userFCC__inscrit='1').order_by('userFCC__dtUpdate')
    compoBdispo = Compo.objects.filter(session__id_session=sessionActive.id_session, equipe='B', userFCC__inscrit='1').order_by('userFCC__dtUpdate')
    absents = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='3').order_by('userFCC__dtUpdate')
    return render(request, 'fcc/compo.html', {'compoAdispo': compoAdispo, 'compoBdispo': compoBdispo, 'absents': absents})


def loginFCC(request):
    """Connexion."""
    if request.user.is_authenticated():
        return render(request, 'fcc/home.html')

    error = False
    next = ""
    if request.GET:
        next = request.GET['next']

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                if next == "":
                    return HttpResponseRedirect('/fcc/home')
                else:
                    return HttpResponseRedirect(next)
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'fcc/login.html', locals())


@login_required
def inscription(request, dispo):
    """Inscription au match."""
    u = request.user
    userFCC = UserFCC.objects.get(user=u)
    if dispo == "1":
            userFCC.inscrit = 1
    else:
        userFCC.inscrit = 3
    userFCC.save()
    return redirect('/fcc/compo')


def addResultats(request):
    """Ajout d'un résultat à un match."""
    idMatch = Match.objects.filter(ouverte=True)[0]
    error = False
    ResultatTeamAFormSet = modelformset_factory(Resultat, ResultatTeamAForm, extra=5)
    ResultatTeamBFormSet = modelformset_factory(Resultat, ResultatTeamBForm, extra=5)
    if request.method == "POST":
        resultat_match = ResultatMatchForm(request.POST, instance=idMatch)
        resultat_teamA_formset = ResultatTeamAFormSet(request.POST, prefix='teamA')
        resultat_teamB_formset = ResultatTeamBFormSet(request.POST, prefix='teamB')
        if resultat_teamA_formset.is_valid() and resultat_teamB_formset.is_valid and resultat_match.is_valid:
            """Enregistrement du résultat du match."""
            resultat_match.id_match = idMatch
            resultat_match.save()
            """Ouverture du match suivant."""
            ancienneJournee = Match.objects.get(id_match=idMatch.id_match)
            ancienneJournee.ouverte = False
            ancienneJournee.save()
            prochaineJournee = Match.objects.filter(ouverte=False, inscrits=0, dateMatch__gt=ancienneJournee.dateMatch).order_by('dateMatch')[0]
            prochaineJournee.ouverte = True
            prochaineJournee.save()
            majInscrits()
            """Calcul de l"équipe gagnante."""
            winA = 2
            winB = 2
            if int(resultat_match.cleaned_data['scoreA']) > int(resultat_match.cleaned_data['scoreB']):
                winA = 1
                winB = 0
            if int(resultat_match.cleaned_data['scoreA']) < int(resultat_match.cleaned_data['scoreB']):
                winA = 0
                winB = 1
            """Enregistrement résultats du FC Carolus."""
            resultatsA = resultat_teamA_formset.save(commit=False)
            for resultatA in resultatsA:
                resultatA.match = idMatch
                resultatA.equipe = 'A'
                majStat(resultatA.userFCC, winA, resultatA.buts, idMatch.session)
            resultat_teamA_formset.save()
            """Enregistrement résultats du SAC."""
            resultatsB = resultat_teamB_formset.save(commit=False)
            for resultatB in resultatsB:
                resultatB.match = idMatch
                resultatB.equipe = 'B'
                majStat(resultatB.userFCC, winB, resultatB.buts, idMatch.session)
            resultat_teamB_formset.save()
            return redirect('/fcc/majclass')
        else:
            error = True
    else:
        resultat_match = ResultatMatchForm()
        resultat_teamA_formset = ResultatTeamAFormSet(queryset=Resultat.objects.none(), prefix='teamA')
        resultat_teamB_formset = ResultatTeamBFormSet(queryset=Resultat.objects.none(), prefix='teamB')
        return render(request, 'fcc/addResults.html', {
            'resultat_match': resultat_match,
            'resultat_teamA_formset': resultat_teamA_formset,
            'resultat_teamB_formset': resultat_teamB_formset,
            })


def majStat(userFCC, win, buts, session):
    """Mise à jour d'un joueur suite à l'enregistrement d'un match."""
    MajStat, created = Stat.objects.get_or_create(userFCC=userFCC, session=session, defaults={"userFCC": userFCC, "session": session})
    if win == 1:
        MajStat.victoire += 1
        MajStat.points += 3
    elif win == 0:
        MajStat.defaite += 1
    elif win == 2:
        MajStat.nul += 1
        MajStat.points += 1
    MajStat.buts += buts
    MajStat.save()


def results(request):
    """Page de résultat d'un match."""
    derniermatch = Match.objects.exclude(inscrits=0).order_by('-dateMatch')[0]
    compoA = Resultat.objects.filter(match=derniermatch, equipe='A').order_by('-buts')
    compoB = Resultat.objects.filter(match=derniermatch, equipe='B').order_by('-buts')
    return render(request, 'fcc/results.html', {'compoA': compoA, 'compoB': compoB, 'match': derniermatch})


def statsBySession(session):
    """Calcul des statistiques."""
    session = Session.objects.filter(id_session=session)
    statsJoueursBySession = Stat.objects.filter(session=session).order_by('classement')
    return statsJoueursBySession


def stats(request):
    """Page des statisiques."""
    session = Session.objects.filter(ouverte=True)[0]
    stats = statsBySession(session.id_session)
    return render(request, 'fcc/stats.html', {'stats': stats, 'session': session})


def majClass(request):
    """Recalcul des classements last et courant."""
    session = Session.objects.filter(ouverte=True)[0]
    stats_a_maj = statsBySession(session.id_session)
    s = sorted(stats_a_maj, key=operator.attrgetter('buts'), reverse=True)
    s2 = sorted(s, key=operator.attrgetter('nb_matchs'), reverse=False)
    s3 = sorted(s2, key=operator.attrgetter('points'), reverse=True)
    i = 1
    for stats in s3:
        stats.classement_last = stats.classement
        stats.classement = i
        stats.save()
        i += 1
    return redirect('/fcc/stats')


def majInscrits():
    """Réinitialisation des informations d'inscription au prochain match."""
    UserFCC.objects.all().update(inscrit=0)


@login_required
def user_logout(request):
    """Déconnexion du site."""
    logout(request)
    return HttpResponseRedirect('login')

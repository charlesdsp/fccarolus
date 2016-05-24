"""
Définition des pages du site.

home, inscrits etc.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from fcc.models import UserFCC, Session, Compo, Match, Resultat, Stat, Award, AwardVainqueur, News, Joker
from fcc.forms import ConnexionForm, ResultatTeamAForm, ResultatTeamBForm, ResultatMatchForm, UserForm, UserFCCForm, YearAwardsForm, NewsForm, JokerForm
import operator

import logging
from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger('sorl.thumbnail').addHandler(handler)


@login_required
def home(request):
    """Page d'accueil."""
    sessionActive = Session.objects.filter(ouverte=True)[0]
    liste_inscrits = UserFCC.objects.filter(inscrit=1)
    liste_absents = UserFCC.objects.filter(inscrit=3)
    liste_en_attente = UserFCC.objects.filter(inscrit=0)
    nb_inscrits = len(liste_inscrits)
    nb_absents = len(liste_absents)
    nb_en_attente = len(liste_en_attente)
    prochainMatch = Match.objects.filter(ouverte=True)[0]
    """Génère un formulaire de news."""
    u = request.user
    userFCC = UserFCC.objects.get(user=u)
    if request.method == "POST":
        print("form passe")
        if request.is_ajax():
            print("ISAJAX")
            # Always use get on request.POST. Correct way of querying a QueryDict.
            titre = request.POST.get('titre')
            print("tITRE" + titre)
            message = request.POST.get('message')
            data = {"titre": titre, "message": message}
            news = News()
            news.userFCC = userFCC
            news.titre = titre
            news.message = message
            news.save()
    news_form = NewsForm()
    liste_news = News.objects.all().order_by('-date')
    return render(request, 'fcc/home.html', {
        'prochainMatch': prochainMatch,
        'sessionActive': sessionActive,
        'nbInscrits': nb_inscrits,
        'nbAbsents': nb_absents,
        'nbAttente': nb_en_attente,
        'news_form': news_form,
        'news': liste_news
    })


def news(request):
    """Affiche les news sur la page d'accueil."""
    liste_news = News.objects.all().order_by('-date')
    return render(request, 'fcc/news.html', {'news': liste_news})


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
    match = Match.objects.filter(ouverte=True)[0]
    if request.method == "POST":
        joker_form = JokerForm(request.POST)
        if joker_form.is_valid():
            joker = Joker()
            joker.joker = joker_form.cleaned_data["joker"]
            u = request.user
            userFCC = UserFCC.objects.get(user=u)
            joker.userFCC = userFCC
            joker.match = match
            joker.save()
    sessionActive = Session.objects.filter(ouverte=True)[0]
    absents = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='3').order_by('userFCC__dtUpdate')
    en_attente = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='0').order_by('userFCC__user__username')
    liste_jokers = Joker.objects.filter(match=match)
    joker_form = JokerForm()
    return render(request, 'fcc/compo.html', {'absents': absents, 'en_attente': en_attente, 'liste_jokers': liste_jokers, 'joker_form': joker_form})


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
    return render(request, 'fcc/results.html', {'match': derniermatch})


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


def awards(request, year=None):
    """Déconnexion du site."""
    annee = year
    if year is None:
        annee = Award.objects.all().order_by('-annee')[0].annee
    if request.method == "POST":
        year_form = YearAwardsForm(data=request.POST)

        if year_form.is_valid():
            annee = year_form.cleaned_data['year']
    liste_awards = Award.objects.filter(annee=annee).order_by('nom_award')
    liste_vainqueurs = AwardVainqueur.objects.filter(award__annee=annee).order_by('award__nom_award')
    year_form = YearAwardsForm(initial={'year': annee})
    print(year_form)
    return render(request, 'fcc/awards.html', {'liste_awards': liste_awards, 'liste_vainqueurs': liste_vainqueurs, 'year': annee, 'year_form': year_form})

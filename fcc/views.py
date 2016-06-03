"""
Définition des pages du site.

home, inscrits etc.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Avg, Sum
from django.http import HttpResponseRedirect
from fcc.models import UserFCC, Session, Compo, Match, Resultat, Stat, Award, AwardVainqueur,\
    News, Joker, NoteMatch
from django.contrib.auth.models import User
from fcc.forms import ConnexionForm, ResultatTeamAForm, ResultatTeamBForm, ResultatMatchForm, UserForm,\
    UserFCCForm, YearAwardsForm, NewsForm, JokerForm, SessionForm
import operator

import logging
from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger('sorl.thumbnail').addHandler(handler)


@login_required
def home(request):
    """Page d'accueil."""
    """Calcul de le compo du prochain match."""
    sessionActive = Session.objects.filter(ouverte=True)[0]
    prochainMatch = Match.objects.filter(ouverte=1)[0]
    nb_inscrits = UserFCC.objects.filter(inscrit=1).count()
    nb_joker = Joker.objects.filter(match=prochainMatch).count()
    nb_inscrits = nb_inscrits + nb_joker
    nb_absents = UserFCC.objects.filter(inscrit=3).count()
    nb_en_attente = UserFCC.objects.filter(inscrit=0, titulaire=True).count()
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
            new_pass = user_form.cleaned_data['password']
            u.set_password(new_pass)
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
        return render(request, 'fcc/user.html', {
            'user': id_user,
            'user_form': user_form,
            'userFCC_form': userFCC_form
            })
    user = get_object_or_404(UserFCC, idUserFCC=id_user)
    return render(request, 'fcc/user.html', {'user': user})


@login_required
def compo(request):
    """Page de la compo du match."""
    match = Match.objects.filter(ouverte=1)[0]
    u = request.user
    userFCC = UserFCC.objects.get(user=u)
    if request.method == "POST":
        joker_form = JokerForm(request.POST)
        if joker_form.is_valid():
            joker = Joker()
            joker.joker = joker_form.cleaned_data["joker"]
            joker.userFCC = userFCC
            joker.match = match
            joker.save()
    sessionActive = Session.objects.filter(ouverte=True)[0]
    absents = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='3')\
        .order_by('userFCC__dtUpdate')
    en_attente = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='0')\
        .order_by('userFCC__user__username')
    liste_invite = UserFCC.objects.filter(titulaire='0', inscrit='1')
    print("Invité ----" + str(liste_invite))
    liste_jokers = Joker.objects.filter(match=match)
    joker_form = JokerForm()
    return render(request, 'fcc/compo.html', {
        'userFCC': userFCC,
        'absents': absents,
        'en_attente': en_attente,
        'liste_jokers': liste_jokers,
        'joker_form': joker_form,
        'liste_invite': liste_invite
        })


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
    idMatch = Match.objects.filter(ouverte=1)[0]
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
            ancienneJournee.ouverte = 2
            ancienneJournee.save()
            try:
                prochaineJournee = Match.objects.filter(ouverte=0, inscrits=0, dateMatch__gt=ancienneJournee.dateMatch)\
                    .order_by('dateMatch')[0]
            except:
                print('Plus de match prévus')
            else:
                prochaineJournee.ouverte = 1
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
    if request.method == "POST":
        print("form passe")
        if request.is_ajax():
            print("ISAJAX")
            # Always use get on request.POST. Correct way of querying a QueryDict.
            j = request.POST.get('joueur')
            print(j)
            joueur = UserFCC.objects.get(pk=j)
            u = request.user
            userFCC = UserFCC.objects.get(user=u)
            m = request.POST.get('match')
            match = Match.objects.get(pk=m)
            note = request.POST.get('note')
            note_match = NoteMatch.objects.filter(userFCC=userFCC, joueur=joueur, match=match)
            if not note_match:
                print("Rien trouvé en base")
                note_match = NoteMatch()
            else:
                note_match = note_match[0]
            note_match.userFCC = userFCC
            note_match.joueur = joueur
            note_match.match = match
            note_match.note = float(note) * 2
            note_match.save()
            majNoteJoueur(joueur, match)
    derniermatch = Match.objects.filter(ouverte=2).order_by('-dateMatch')[0]
    notes_match = NoteMatch.objects.filter(match=derniermatch)
    return render(request, 'fcc/results.html', {'match': derniermatch, "notes_match": notes_match})


def session(request, session=None):
    """Page des sessions."""
    s = session
    if s is None:
        session = Session.objects.filter(ouverte=True)[0]
    else:
        session = Session.objects.get(pk=s)
    liste_match = Match.objects.filter(session=session).order_by('dateMatch')
    win_FCC = 0
    win_SAC = 0
    draw = 0
    for match in liste_match:
        if match.ouverte == 2:
            print(match.id_match)
            if match.scoreA > match.scoreB:
                win_FCC = win_FCC + 1
            elif match.scoreA < match.scoreB:
                win_SAC = win_SAC + 1
            else:
                draw = draw + 1
    liste_old_session = Session.objects.filter(ouverte=False)
    for old_session in liste_old_session:
        old_session.debut = Match.objects.filter(session=old_session)[0].dateMatch
        try:
            old_session.leader = Stat.objects.filter(session=old_session).order_by('classement')[0]
        except:
            print("Pas de leader")
            old_session.leader = None
    leaders = Stat.objects.filter(session=session).order_by('classement')[:2]
    return render(request, 'fcc/session.html', {
        'session': session,
        'win_FCC': win_FCC,
        'win_SAC': win_SAC,
        'draw': draw,
        'liste_match': liste_match,
        'liste_old_session': liste_old_session,
        'leaders': leaders
        })


def statsBySession(session):
    """Calcul des statistiques."""
    session = Session.objects.filter(id_session=session)
    statsJoueursBySession = Stat.objects.filter(session=session).order_by('classement')
    return statsJoueursBySession


def stats(request, s=None):
    """Page des statisiques."""
    session = s
    if s is None:
        session = Session.objects.filter(ouverte=True)[0]
    if request.method == "POST":
        session_form = SessionForm(data=request.POST)

        if session_form.is_valid():
            session_envoyee = session_form.cleaned_data['s']
            if session_envoyee == 'Global':
                stats_globales = Stat.objects.values('userFCC').annotate(
                    points=Sum('points'),
                    victoire=Sum('victoire'),
                    defaite=Sum('defaite'),
                    nul=Sum('nul'),
                    buts=Sum('buts')
                    )
                for stat in stats_globales:
                    stat['note'] = 0
                    note = Resultat.objects.filter(userFCC=stat['userFCC']).aggregate(Avg('moyenne_note'))['moyenne_note__avg']
                    stat['note'] = note
                return render(request, 'fcc/stats.html', {'stats': stats_globales, 'session': session})
            else:
                session = Session.objects.get(pk=session_envoyee)
    stats = statsBySession(session.id_session)
    if not stats:
        session_precedente = session.id_session - 1
        stats = statsBySession(session_precedente)
    for stat in stats:
        stat.note = 0
        list_match = Match.objects.filter(session=session)
        note = Resultat.objects.filter(userFCC=stat.userFCC, match__in=list_match)\
            .aggregate(Avg('moyenne_note'))['moyenne_note__avg']
        stat.note = note
    session_form = SessionForm(initial={'s': session.id_session})
    return render(request, 'fcc/stats.html', {'stats': stats, 'session': session, 'session_form': session_form})


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


def majNoteJoueur(joueur, match):
    """Recalcul de la note moyenne d'un joueur."""
    result = Resultat.objects.filter(userFCC=joueur, match=match)[0]
    result.moyenne_note = NoteMatch.objects.filter(joueur=joueur, match=match).aggregate(Avg('note'))['note__avg']
    result.save()


def majInscrits():
    """Réinitialisation des informations d'inscription au prochain match."""
    UserFCC.objects.all().update(inscrit=0)


@login_required
def user_logout(request):
    """Déconnexion du site."""
    logout(request)
    return HttpResponseRedirect('login')


def awards(request, year=None):
    """Awards."""
    annee = year
    if year is None:
        annee = Award.objects.all().order_by('-annee')[0].annee
    if request.method == "POST":
        year_form = YearAwardsForm(data=request.POST)

        if year_form.is_valid():
            annee = year_form.cleaned_data['year']
    liste_awards = Award.objects.filter(annee=annee).order_by('id_award')
    liste_vainqueurs = AwardVainqueur.objects.filter(award__annee=annee).order_by('award__nom_award')
    year_form = YearAwardsForm(initial={'year': annee})
    return render(request, 'fcc/awards.html', {
        'liste_awards': liste_awards, 'liste_vainqueurs': liste_vainqueurs, 'year': annee, 'year_form': year_form
        })


def majNoteInit():
    """Recalcul de toutes les notes."""
    liste_match = Match.objects.all()
    for match in liste_match:
        liste_resultats = Resultat.objects.filter(match=match)
        for result in liste_resultats:
            result.moyenne_note = NoteMatch.objects.filter(joueur=result.userFCC, match=result.match).aggregate(Avg('note'))['note__avg']
            if result.moyenne_note is None:
                result.moyenne = 0.00
            result.save()


def relance(request):
    """Relance pour l'inscription au match."""
    prochainMatch = Match.objects.filter(ouverte=1)[0]
    nb_inscrits = UserFCC.objects.filter(inscrit=1).count()
    nb_joker = Joker.objects.filter(match=prochainMatch).count()
    nb_inscrits = nb_inscrits + nb_joker
    nb_absents = UserFCC.objects.filter(inscrit=3).count()
    nb_en_attente = UserFCC.objects.filter(inscrit=0, titulaire=True).count()
    liste_mail = User.objects.filter(email__contains='@').values_list('email', flat=True)
    print(type(liste_mail))
    sujet = 'Relance : ' + str(nb_inscrits) + ' inscrits | ' \
        + str(nb_absents) + ' absents | ' \
        + str(nb_en_attente) + ' en attente'
    html = get_template('fcc/relance.html')

    d = (
            {
                'prochainMatch': prochainMatch,
                'nbInscrits': nb_inscrits,
                'nbAbsents': nb_absents,
                'nbAttente': nb_en_attente
            }
        )
    message_text = html.render(d)
    message_html = html.render(d)
    msg = EmailMultiAlternatives(sujet, message_text, 'fccarolus@fccarolus.com', liste_mail)
    msg.attach_alternative(message_html, "text/html")
    msg.send()
    return redirect('/fcc/home')

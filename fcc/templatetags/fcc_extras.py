"""Tags spécifiques au site FCC."""
from django import template
from fcc.models import Session, Compo, Resultat, Match, UserFCC

register = template.Library()


@register.inclusion_tag('fcc/compo_equipe.html')
def get_compo_equipe(**kwargs):
    """Page de la compo du match."""
    equipe = kwargs['equipe']
    sessionActive = Session.objects.filter(ouverte=True)[0]
    if equipe == "C":
        compo_equipe = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='3').order_by('userFCC__dtUpdate')
        liste_invite_abs = UserFCC.objects.filter(titulaire='0', inscrit='3')
        return {'compo_equipe': compo_equipe, 'liste_invite_abs': liste_invite_abs}
    if equipe == "D":
        compo_equipe = Compo.objects.filter(session__id_session=sessionActive.id_session, userFCC__inscrit='0').order_by('userFCC__user__username')
        liste_invite_abs = UserFCC.objects.filter(titulaire='0', inscrit='3')
        return {'compo_equipe': compo_equipe}
    compo_equipe = Compo.objects.filter(session__id_session=sessionActive.id_session, equipe=equipe, userFCC__inscrit='1').order_by('userFCC__dtUpdate')
    return {'compo_equipe': compo_equipe}


@register.inclusion_tag('fcc/resultat_equipe.html')
def get_resultat_equipe(**kwargs):
    """Page de résultat d'un match."""
    equipe = kwargs['equipe']
    m = kwargs['m']
    old = kwargs['old']
    match = Match.objects.get(pk=m)
    result_equipe = Resultat.objects.filter(match=match, equipe=equipe).order_by('-buts')
    return {'result_equipe': result_equipe, 'm': m, 'old': old}

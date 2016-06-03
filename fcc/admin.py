"""Admin Django."""

from django.contrib import admin
from .models import UserFCC, Match, Session, Resultat, Stat, Compo, Award, AwardVainqueur, News

admin.site.register(UserFCC)
admin.site.register(Match)
admin.site.register(Session)
admin.site.register(Resultat)
admin.site.register(Stat)
admin.site.register(Compo)
admin.site.register(Award)
admin.site.register(AwardVainqueur)
admin.site.register(News)

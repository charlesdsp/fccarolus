"""Admin Django."""

from django.contrib import admin
from .models import UserFCC, Match, Session, Resultat, Stat, Compo, Award, AwardVainqueur, News, Joker


class UserFCCAdmin(admin.ModelAdmin):
    list_display = ('user', 'inscrit', 'titulaire')
    list_filter = ('inscrit', 'titulaire',)
    ordering = ('user', )
    search_fields = ('user', 'inscrit')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id_match', 'dateMatch', 'ouverte', 'inscrits', 'session')
    list_filter = ('ouverte', 'session',)
    ordering = ('-id_match', )


class JokerAdmin(admin.ModelAdmin):
    list_display = ('match', 'joker', 'userFCC')
    list_filter = ('match',)
    ordering = ('-match', )

admin.site.register(UserFCC, UserFCCAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Session)
admin.site.register(Resultat)
admin.site.register(Stat)
admin.site.register(Compo)
admin.site.register(Award)
admin.site.register(AwardVainqueur)
admin.site.register(News)
admin.site.register(Joker)

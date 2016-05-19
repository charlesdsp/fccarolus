"""Admin Django."""

from django.contrib import admin

# Register your models here.

from .models import UserFCC, Match, Session, Resultat, Stat, Compo

admin.site.register(UserFCC)
admin.site.register(Match)
admin.site.register(Session)
admin.site.register(Resultat)
admin.site.register(Stat)
admin.site.register(Compo)

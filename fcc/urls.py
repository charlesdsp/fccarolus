"""
Liste des url.

home, inscrits etc.
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^user/(?P<id_user>\d+)$', views.user),
    url(r'^user/$', views.user),
    url(r'^compo$', views.compo),
    url(r'^results$', views.results),
    url(r'^stats$', views.stats),
    url(r'^majclass$', views.majClass),
    url(r'^login$', views.loginFCC),
    url(r'^inscription/(?P<dispo>\d+)$', views.inscription),
    url(r'^addResults$', views.addResultats),
]

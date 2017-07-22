"""
Liste des url.

home, inscrits etc.
"""

from django.conf.urls import url
from . import views, passwordReset
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home),
    url(r'^home$', views.home),
    url(r'^user/(?P<id_user>\d+)$', views.user),
    url(r'^user/$', views.user),
    url(r'^compo$', views.compo),
    url(r'^results$', views.results),
    url(r'^stats$', views.stats),
    url(r'^majclass$', views.majClass),
    url(r'^raz$', views.raz),
    url(r'^login$', views.loginFCC),
    url(r'^inscription/(?P<dispo>\d+)$', views.inscription),
    url(r'^addResults$', views.addResultats),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^awards$', views.awards),
    url(r'^session/(?P<session>\d+)$', views.session),
    url(r'^session$', views.session),
    url(r'^news$', views.news, name='news'),
    url(r'^invites$', views.invites, name='invites'),
    url(r'^relance$', views.relance),
    url(r'^supp_news$', views.supp_news),
    url(r'^supp_joker$', views.supp_joker),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', passwordReset.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^password', passwordReset.ResetPasswordRequestView.as_view(), name="reset_password")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

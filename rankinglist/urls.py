from django.urls import path
from django.conf.urls import url

from .forms import MatchNewWizardForm1, MatchNewWizardForm2,MatchNewWizardForm3
from .views import MatchNewWizard

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('rankinglist/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
    path('match/history', views.matcheshistory, name='matcheshistory'),
    path('signup', views.signup ,name='signup'),
    url(r'^match/new/wizard$', MatchNewWizard.as_view([MatchNewWizardForm1, MatchNewWizardForm2,MatchNewWizardForm3])),
]
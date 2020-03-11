from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from .forms import MatchNewWizardForm1, MatchNewWizardForm2,MatchNewWizardForm3
from .views import MatchNewWizard, MatchCreateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('rankinglist/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
    path('match/history', views.matcheshistory, name='matcheshistory'),
    path('match/create/<int:r_id>', MatchCreateView.as_view() , name='matchcreate'),
    path('signup', views.signup ,name='signup'),
    url(r'^match/new/wizard$', MatchNewWizard.as_view([MatchNewWizardForm1, MatchNewWizardForm2,MatchNewWizardForm3])),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
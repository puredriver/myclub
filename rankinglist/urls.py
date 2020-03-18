from django.urls import path, include

from . import views
from .routers import ReadOnlyRouter
from .viewsets import MatchViewSet, RankinglistViewSet

router = ReadOnlyRouter()
router.register('match', MatchViewSet)
router.register('rankinglist', RankinglistViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('rankinglist/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
    path('match/history', views.matcheshistory, name='matcheshistory'),
]
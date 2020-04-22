from django.urls import path, include

from . import views
from .routers import ReadOnlyRouter
from .viewsets import RankinglistViewSet

router = ReadOnlyRouter()
router.register('rankinglist', RankinglistViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('club/<int:club_id>', views.clubmain, name='clubmain'),
    path('club/<int:club_id>/player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('club/<int:club_id>/rankinglist/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
   # path('club/<int:club_id>/match/history', views.matcheshistory, name='matcheshistory'),
]
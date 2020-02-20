from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('rankinglist/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
]
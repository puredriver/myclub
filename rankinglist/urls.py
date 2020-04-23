from django.urls import path, include, re_path

from . import views
from django.contrib.auth import views as auth_views
from .routers import ReadOnlyRouter
from .viewsets import RankinglistViewSet

router = ReadOnlyRouter()
router.register('rankinglist', RankinglistViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('club/<int:club_id>', views.clubmain, name='clubmain'),
    path('club/<int:club_id>/player/<int:player_id>/history', views.playerhistory, name='player_history'),
    path('club/<int:club_id>/rl/<int:rankinglist_id>/stats', views.rankingliststats, name='rankinglist_stats'),
    # path('club/<int:club_id>/match/history', views.matcheshistory, name='matcheshistory'),
    path("signup", views.signup, name='signup'),
    # re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('login', auth_views.LoginView.as_view(template_name='rankinglist/login.html'),name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='rankinglist/logout.html'),name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

   
]
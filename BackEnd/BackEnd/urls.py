"""BackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from Players import views as players


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/teams', players.TeamList.as_view()),
    url(r'^api/v1/team/(?P<pk>[0-9]+)$', players.TeamDetail.as_view()),
    url(r'^api/v1/players/(?P<pk>[0-9]+)$', players.PlayerList.as_view()),
    url(r'^api/v1/player/(?P<pk>[0-9]+)$', players.PlayerDetail.as_view()),
    url(r'^api/v1/player/batter/(?P<pk>[0-9]+)$', players.PlayerBatterDetail.as_view()),
    url(r'^api/v1/player/pitcher/(?P<pk>[0-9]+)$', players.PlayerPitcherDetail.as_view()),
    url(r'^api/v1/batters/(?P<pk>[0-9]+)$', players.BatterList.as_view()),
    url(r'^api/v1/batter/(?P<pk>[0-9]+)$', players.BatterDetail.as_view()),
    url(r'^api/v1/pitchers/(?P<pk>[0-9]+)$', players.PitcherList.as_view()),
    url(r'^api/v1/pitcher/(?P<pk>[0-9]+)$', players.PitcherDetail.as_view()),
]

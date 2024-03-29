"""FrontEnd URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from views import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.teamSelect),
    url(r'^updateTeamSelect/(?P<pk>[0-9]+)$', views.updateTeamSelect),
    url(r'^create/team', views.createTeam),
    url(r'^create/roster', views.createRoster),
    url(r'^teams', views.viewTeams),
    url(r'^team/(?P<pk>[0-9]+)$', views.viewTeam),
    url(r'^players', views.viewPlayers),
    url(r'^player/(?P<pk>[0-9]+)$', views.viewPlayer),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

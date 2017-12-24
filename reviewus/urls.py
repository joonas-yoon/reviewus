"""reviewus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^accounts/', include('accounts.urls', namespace='accounts')),
  url(r'^program/', include('program.urls', namespace='program')),
  url(r'^broadcasts/', include('broadcastsystem.urls', namespace='broadcasts')),
  url(r'^jihoon/', include('jihoon.urls', namespace='jihoon')),
  url(r'', include('django.contrib.auth.urls')),
  url(r'', include('home.urls')),
  url(r'', include('episode.urls', namespace='episode')),
  url(r'', include('social_django.urls', namespace='social'))
]


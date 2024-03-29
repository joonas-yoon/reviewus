from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^signup/$', views.signup, name='signup'),
  url(r'^logout/$', auth_views.logout, {'next_page' : '/'}),
]

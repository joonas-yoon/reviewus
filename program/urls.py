from django.conf.urls import include, url

from . import views

app_name = 'program'

urlpatterns = [
  url(r'^create/$', views.create, name='create'),
  url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
  url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
  url(r'^list(?:/(?P<page>\d+))?/$', views.list, name='list'),

  url(r'^casting/(?P<id>\d+)/add/$', views.add_cast, name='add_cast'),

  url(r'^(?P<id>\d+)/$', views.view, name='view'),
]

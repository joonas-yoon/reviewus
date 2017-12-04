from django.conf.urls import url

from . import views

app_name = 'program'

urlpatterns = [
  url(r'^create/$', views.create, name='create'),
  url(r'^list(?:/(?P<page>\d+))?/$', views.list, name='list'),
  url(r'^(?P<id>\d+)/$', views.view, name='view'),
]

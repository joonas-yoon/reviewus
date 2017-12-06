from django.conf.urls import include, url

from . import views

app_name = 'episode'

urlpatterns = [
  url(r'^episode/', include([
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^list(?:/(?P<page>\d+))?/$', views.list, name='list'),
    url(r'^(?P<id>\d+)/$', views.view, name='view'),
  ])),

  url(r'^program/(?P<program_id>\d+)/episode/', include([
    url(r'^add/$', views.create_with_program, name='create_with_program'),
    url(r'^(?P<nth>\d+)/$', views.view_nth_with_program, name='view_nth_with_program'),
  ])),
]

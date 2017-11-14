from django.conf.urls import url

from home import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^(?P<echo_msg>\w+)/$', views.echo, name='echo'),
]

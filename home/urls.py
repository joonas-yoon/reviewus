from django.conf.urls import url
from django.contrib.auth import views as auth_views

from home import views

app_name = 'home'

urlpatterns = [
  url(r'^$', views.index, name='index'),

  url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

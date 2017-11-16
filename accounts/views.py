from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def signup(request):
  return render(request, 'registration/signup.html');


def index(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('login'))
  
  return HttpResponse("Welcome %s" % request.user.username)


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import login

from datetime import datetime, timezone, timedelta


def index(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('accounts:index'))

  return render(request, 'home/index.html')



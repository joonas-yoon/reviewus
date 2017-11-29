from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import login, authenticate
from .forms import SignupForm, LoginForm

from reviewus.db import DBManager as DB


def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)
      return HttpResponseRedirect(reverse('accounts:index'))
  else:
    form = SignupForm()

  return render(request, 'registration/signup.html', {
    'form': form
  })


def index(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('login'))

  sql = 'SELECT * FROM ru_review WHERE author_id = %d' % request.user.id
  my_reviews = DB.execute_and_fetch_all(sql, as_list=True)
  
  return render(request, 'accounts/index.html', {
    'user': request.user,
    'reviews': my_reviews
  })


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

  sql = 'SELECT R.*, P.id AS program_id, P.title AS program_title,\
      E.id AS episode_id, E.title AS episode_title\
  FROM\
      ru_review AS R, ru_program AS P, ru_episode AS E\
  WHERE\
      R.episode_id = E.id AND E.program_id = P.id AND R.author_id = %s'

  my_reviews = DB.execute_and_fetch_all(sql, param=(request.user.id), as_list=True)
  
  return render(request, 'accounts/index.html', {
    'user': request.user,
    'reviews': my_reviews
  })


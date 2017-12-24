from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from reviewus.db import DBManager as DB


def index(request):
  if not request.user.is_authenticated():
    return render(request, 'home/index.html')

  sql = 'SELECT R.*, U.username, U.first_name, U.last_name, E.title as episode_title, E.program_id, \
             P.title as program_title \
         FROM ru_review as R, auth_user as U, ru_episode as E, ru_program as P \
         WHERE R.author_id = U.id AND R.episode_id = E.id AND E.program_id = P.id \
         ORDER BY R.creation_time desc \
         LIMIT 10'
  user_reviews = DB.execute_and_fetch_all(sql, as_list=True)

  statistic = {
    'reviews': 0, 'episodes': 0, 'stars': 0
  }

  for row in user_reviews:
    name = row['last_name']
    for i in row['first_name'] or []:
      name += '*'
    row['display_name'] = name

  try:
    sql = 'SELECT count(id) as count FROM ru_episode'
    statistic['episodes'] = DB.execute_and_fetch(sql, as_row=True)['count']

    sql = 'SELECT count(id) as count, sum(star) as stars FROM ru_review'
    row = DB.execute_and_fetch(sql, as_row=True)
    statistic['reviews'] = row['count']
    statistic['stars'] = row['stars']
  except:
    pass

  return render(request, 'home/main.html', {
    'user': request.user,
    'user_reviews': user_reviews,
    'statistic': statistic
  })


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from reviewus.db import DBManager as DB


def index(request):
  if not request.user.is_authenticated():
    return render(request, 'home/index.html')

  sql = 'SELECT R.*, U.username, E.title as episode_title, P.title as program_title \
         FROM ru_review as R, auth_user as U, ru_episode as E, ru_program as P \
         WHERE R.author_id = U.id AND R.episode_id = E.id AND E.program_id = P.id \
         ORDER BY R.creation_time desc \
         LIMIT 10'
  """
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute(sql)
  result = list(cursor.fetchall())
  fields = [col[0] for col in list(cursor.description)]
  user_reviews = [
    dict(zip(fields, row)) for row in result
  ]
  """
  user_reviews = DB.execute_and_fetch_all(sql, as_list=True)

  return render(request, 'home/main.html', {
    'user': request.user,
    'user_reviews': user_reviews
  })


from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime, timezone, timedelta

def index(request):
  tz = 9
  now = datetime.time(datetime.now(timezone(timedelta(hours=tz))))
  current_time = "%02d:%02d:%02d</h1>" % (now.hour, now.minute, now.second)
  context = {
    'current_time': current_time,
    'now': now
  }

  return render(request, 'home/index.html', context)

def echo(request, echo_msg):
  res = "<h1>Hello, %s</h1>"
  return HttpResponse(res % echo_msg)


from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from reviewus.db import DBManager as DB
import reviewus.apis as API

@login_required
def list(request, page = 1):
    return render(request, 'program/list.html', {
        'programs': API.get_program_list(page, 5)
    })


def view(request, id):
    return render(request, 'program/view.html', {
        'program': API.get_program(id)
    })


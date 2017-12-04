from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request, page):
    return render(request, 'program/list.html', {
        'programs': API.get_program_list(page)
    })


@login_required
def create(request):
    if request.method != 'POST':
        broadcastings = API.get_broadcastsystem_list()
        genres = API.get_genre_list()

        return render(request, 'program/create.html', {
            'broadcastings': broadcastings,
            'genres': genres
        })

    new_program_id = API.create_program(request.body)
    if new_program_id is None:
        return HttpResponse('Invalid Form')

    return HttpResponseRedirect(reverse('program:view', kwargs= {'id': new_program_id}))


def view(request, id):
    return render(request, 'program/view.html', {
        'program': API.get_program(id)
    })


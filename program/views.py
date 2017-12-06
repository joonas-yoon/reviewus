from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request, page):
    cur_page = int(page or 1)
    programs = API.get_programs(page, 12)

    if not programs:
        raise Http404

    return render(request, 'program/list.html', {
        'page': {
            'prev': max(1, cur_page - 1),
            'cur' : cur_page,
            'next': cur_page + 1
        },
        'programs': programs
    })


@staff_member_required
def create(request):
    if request.method != 'POST':
        broadcastings = API.get_broadcastsystems()
        genres = API.get_genres()

        return render(request, 'program/form.html', {
            'method': 'create',
            'broadcastings': broadcastings,
            'genres': genres
        })

    new_program_id = API.create_program(request.body)
    if new_program_id is None:
        return HttpResponse('Invalid Form')

    return redirect('program:view', id= new_program_id)


@staff_member_required
def edit(request, id):
    program = API.get_program(id)

    if not program:
        raise Http404

    if request.method != 'POST':
        broadcastings = API.get_broadcastsystems()
        genres = API.get_genres()

        return render(request, 'program/form.html', {
            'method': 'edit',
            'broadcastings': broadcastings,
            'genres': genres,
            'program': program
        })

    if API.update_program(request.body, id= id) is not None:
        return redirect('program:view', id= id)
    else:
        return HttpResponse('Invalid Form')


def view(request, id):
    program = API.get_program(id)

    if not program:
        raise Http404

    return render(request, 'program/view.html', {
        'program': program
    })


@staff_member_required
def delete(request, id):
    program = API.get_program(id)

    if not program:
        raise Http404

    if request.method == 'POST':
        API.delete_program(id)
        return redirect('program:list')

    else:
        return render(request, 'program/delete.html', {
            'program': program
        })






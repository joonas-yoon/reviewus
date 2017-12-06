from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request, page):
    cur_page = int(page or 1)
    episodes = API.get_episodes(page)

    if not episodes:
        raise Http404

    for ep in episodes:
        sql = 'SELECT AVG(star) AS avg_star, COUNT(star) AS total_star \
               FROM ru_review \
               WHERE episode_id = %s'
        ep['reviews'] = DB.execute_and_fetch(sql, param=(ep['id']), as_row=True)
        ep['program'] = API.get_program(ep['program_id'])

    return render(request, 'episode/list.html', {
        'page': {
            'prev': max(1, cur_page - 1),
            'cur' : cur_page,
            'next': cur_page + 1
        },
        'episodes': episodes
    })


@staff_member_required
def create(request):
    pass


def view(request, id):
    return HttpResponse("id is " + id)


@staff_member_required
def edit(request, id):
    pass


@staff_member_required
def delete(request, id):
    pass


"""
###############################
#
# with program id
#
###############################
"""
def create_with_program(request, program_id):
    program = API.get_program(program_id)

    if not program:
        raise Http404

    if request.method == 'POST':
        epi = API.create_episode(request.body)

        if not epi:
              raise Http404

        return redirect('program:view', id=program_id)

    return render(request, 'episode/form.html', {
        'program': program
    })


def view_with_program(request, program_id, nth):
    program = API.get_program(program_id)

    if not program:
        raise Http404

    return redirect('program:view', id= program_id)


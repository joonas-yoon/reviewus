from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request):
    p = API.get_people()

    if not p:
        raise Http404

    return render(request, 'person/list.html', {
        'people': p
    })


@staff_member_required
def create(request):
    jobs = API.get_jobs()

    if request.method != 'POST':
        return render(request, 'person/form.html', {
            'method': 'create',
            'jobs': jobs
        })

    new_id = API.create_person(request.body)
    if new_id is None:
        return HttpResponse('Invalid Form')

    return redirect('person:view', id= new_id)


@staff_member_required
def edit(request, id):
    jobs = API.get_jobs()
    p = API.get_person(id)

    if not p:
        raise Http404

    if request.method != 'POST':
        return render(request, 'person/form.html', {
            'method': 'edit',
            'person': p,
            'jobs': jobs
        })

    if API.update_person(request.body, id= id) is not None:
        return redirect('person:view', id= id)
    else:
        return HttpResponse('Invalid Form')


def view(request, id):
    sql = 'SELECT P.*, J.id as job_id, J.name as job_name\
    FROM\
        ru_person AS P\
            LEFT JOIN\
        ru_job AS J ON P.job_id = J.id\
    WHERE P.id = %s'

    p = DB.execute_and_fetch(sql, param=(id,), as_row=True)

    """
    sql = 'SELECT DISTINCT E.* \
    FROM ru_cast AS C, ru_episode AS E \
    WHERE C.episode_id = E.id AND C.person_id = %s'
    """
    sql = 'SELECT C.*, P.*, E.id as episode_id, E.title as episode_title \
    FROM ru_cast AS C, ru_episode AS E, ru_program AS P \
    WHERE C.episode_id = E.id AND E.program_id = P.id AND C.person_id = %s \
    ORDER BY P.title'
    epi = DB.execute_and_fetch_all(sql, param=(id,), as_list=True)

    return render(request, 'person/view.html', {
        'person': p,
        'episodes': epi
    })


@staff_member_required
def delete(request, id):
    try:
        res = API.delete_broadcastsystem(id)
        pass
    except:
        pass
    return redirect('broadcasts:list')



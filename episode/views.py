from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def get_review_info(episode_id):
    sql = 'SELECT AVG(star) AS avg_star, COUNT(star) AS total_star \
           FROM ru_review \
           WHERE episode_id = %s'
    try:
        res = DB.execute_and_fetch(sql, param=(episode_id), as_row=True)
    except:
        pass
    return res


def list(request, page):
    cur_page = int(page or 1)
    episodes = API.get_episodes(page)

    if not episodes:
        raise Http404

    for ep in episodes:
        ep['reviews'] = get_review_info(ep['id'])
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
    eid = int(id or 0)
    episode = API.get_episode(eid)

    if not episode:
        raise Http404

    episode['reviews'] = get_review_info(eid)
    program = API.get_program(episode['program_id'])

    sql = 'SELECT R.*, U.username, E.title as episode_title, E.program_id, \
             P.title as program_title \
           FROM ru_review as R, auth_user as U, ru_episode as E, ru_program as P \
           WHERE R.author_id = U.id AND R.episode_id = E.id AND E.program_id = P.id \
           ORDER BY R.creation_time desc \
           LIMIT 10'

    reviews = DB.execute_and_fetch_all(sql, as_list=True) 

    return render(request, 'episode/view.html', {
        'episode': episode,
        'program': program,
        'reviews': reviews
    })


@staff_member_required
def edit(request, id):
    eid = int(id or 0)
    episode = API.get_episode(eid)

    if not episode:
        raise Http404

    if request.method == 'POST':
        if API.update_episode(request.body, id= id) is None:
            raise Http404

        return redirect('episode:view', id= id)

    program = API.get_program(episode['program_id'])

    return render(request, 'episode/edit.html', {
        'episode': episode,
        'program': program
    })


@staff_member_required
def delete(request, id):
    eid = int(id or 0)
    episode = API.get_episode(eid)

    if not episode:
        raise Http404

    if request.method == 'POST':
        API.delete_episode(eid)
        return redirect('episode:list')

    sql = 'SELECT COUNT(id) as reviews FROM ru_review WHERE episode_id = %s'
    res = DB.execute_and_fetch(sql, param=(eid), as_row=True)
    episode['reviews'] = res['reviews']

    return render(request, 'episode/delete.html', {
        'episode': episode,
        'program': API.get_program(episode['program_id'])
    })


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


def view_nth_with_program(request, program_id, nth):
    program = API.get_program(program_id)

    if not program:
        raise Http404

    return redirect('program:view', id= program_id)


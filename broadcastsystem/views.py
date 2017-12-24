from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request):
    bs = API.get_broadcastsystems()

    if not bs:
        raise Http404

    return render(request, 'broadcastsystem/list.html', {
        'broads': bs
    })


@staff_member_required
def create(request):
    if request.method != 'POST':
        return render(request, 'broadcastsystem/form.html', {
            'method': 'create'
        })

    new_id = API.create_broadcastsystem(request.body)
    if new_id is None:
        return HttpResponse('Invalid Form')

    return redirect('broadcasts:list')


@staff_member_required
def edit(request, id):
    bs = API.get_broadcastsystem(id)

    if not bs:
        raise Http404

    if request.method != 'POST':
        return render(request, 'broadcastsystem/form.html', {
            'method': 'edit',
            'broadcast': bs
        })

    if API.update_broadcastsystem(request.body, id= id) is not None:
        return redirect('broadcasts:view', id= id)
    else:
        return HttpResponse('Invalid Form')


def view(request, id):
    bs = API.get_broadcastsystem(id)

    if not bs:
        raise Http404

    sql = 'SELECT P.* \
    FROM ru_broadcast_system AS B, ru_program AS P \
    WHERE B.id = P.broadcast_id AND B.id = %s'
    programs = None
    try:
        programs = DB.execute_and_fetch_all(sql, param=(id,), as_list=True)
    except:
        pass

    sql = 'SELECT avg(star) as avg_star\
    FROM\
        ru_review AS R,\
        ru_broadcast_system AS B,\
        ru_episode AS E,\
        ru_program AS P\
    WHERE\
        R.episode_id = E.id\
            AND E.program_id = P.id\
            AND P.broadcast_id = B.id\
            AND B.id = %s\
    GROUP BY broadcast_id'
    avg_star = None
    try:
        row = DB.execute_and_fetch(sql, param=(id,), as_row=True)
        avg_star = row['avg_star']
    except:
        pass
    bs['avg_star'] = avg_star

    return render(request, 'broadcastsystem/view.html', {
        'broadcast': bs,
        'programs': programs
    })


@staff_member_required
def delete(request, id):
    try:
        res = API.delete_broadcastsystem(id)
        pass
    except:
        pass
    return redirect('broadcasts:list')



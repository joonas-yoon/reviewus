from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from reviewus.db import DBManager as DB
import reviewus.apis as API


def list(request, page=1):
    page = int(page or 1)
    lst = API.get_reviews(page)

    if not lst:
        raise Http404

    return render(request, 'review/list.html', {
        'reviews': lst
    })


@login_required
def create(request):
    if request.method != 'POST':
        raise Http404

    new_id = API.create_review(request.body, request.user.id)
    if new_id is None:
        return HttpResponse('Invalid Form')

    try:
        eid = API.query_from_request(request.body).get('episode_id')
        return redirect('review:list', eid)
    except:
        raise Http404


@login_required
def edit(request, id):
    r = API.get_review(id)

    if not r:
        raise Http404

    if request.method != 'POST':
        return render(request, 'review/form.html', {
            'review': r
        })

    if API.update_review(request.body, id= id) is not None:
        return redirect('review:list')
    else:
        return HttpResponse('Invalid Form')


def view(request, id):
    pass


@login_required
@staff_member_required
def delete(request, id):
    try:
        res = API.delete_review(id)
        pass
    except:
        pass
    return redirect('review:list')



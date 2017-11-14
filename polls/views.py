from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def result(request, question_id):
    return HttpResponse("Result with #" + question_id)

def vote(request, question_id):
    return HttpResponse("Vote with #" + question_id)

def detail(request, question_id):
    return HttpResponse("Detail with #" + question_id)


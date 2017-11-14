from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


# /polls/
class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """Return the last five published questions."""
    return Question.objects.order_by('-pub_date')[:5]


# /polls/1
class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'


# /polls/1/results
class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'


# /polls/1/vote
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "you didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


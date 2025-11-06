from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.db import IntegrityError

from .models import Choice, Question, VoterRecord


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        voter_name = request.POST['voter_name'].strip() # Get the username and strip whitespace
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    except KeyError:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You must enter a username to vote.",
        })

    if not voter_name:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Username cannot be empty. Please enter your username.",
        })

    if VoterRecord.objects.filter(question=question, voter_name=voter_name).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': f"The user '{voter_name}' has already voted in this poll.",
        })

    try:
        selected_choice.votes += 1
        selected_choice.save()

        VoterRecord.objects.create(question=question, voter_name=voter_name)

    except IntegrityError:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': f"A database error occurred. It seems '{voter_name}' has already voted.",
        })

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
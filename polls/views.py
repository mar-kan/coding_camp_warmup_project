from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import F
from django.db.models import Sum
from django.db.models.functions import Coalesce
import json
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


def poll_piechart(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()

    texts = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]

    data = {
        'question': question,
        'choices': json.dumps(texts),
        'votes': json.dumps(votes)
    }
    return render(request, "polls/results.html", data)

#def index(request):
#    latest_question_list = Question.objects.order_by("-pub_date")[:5]
#    return render(request, "polls/index.html", {"latest_question_list": latest_question_list})

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/detail.html", {"question": question})


def stats(request):
    # Per-question totals; treat NULL as 0
    questions = Question.objects.annotate(total_votes=Coalesce(Sum("choice__votes"), 0))
    totals = questions.aggregate(all_votes=Coalesce(Sum("choice__votes"), 0))
    context = {
        "questions": questions.order_by("-total_votes", "-pub_date"),
        "all_votes": totals["all_votes"],
        "question_count": questions.count(),
    }
    return render(request, "polls/stats.html", context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Prevent voting if poll is closed
    if not question.is_open:
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "This poll is closed. Voting is disabled."},
        )


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

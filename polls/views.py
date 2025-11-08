from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question, Choice
from django.db.models import Sum
from django.db.models.functions import Coalesce


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    return render(request, "polls/index.html", {"latest_question_list": latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

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
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn’t select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

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


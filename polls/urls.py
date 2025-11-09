from django.urls import path
from . import views


app_name = "polls"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:question_id>/results/", views.poll_piechart, name="results"),
    #path("", views.index, name="index"),
    #path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("stats/", views.stats, name="stats"),


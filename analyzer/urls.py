from django.urls import path
from . import views

app_name = "analyzer"

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start_quiz, name="start_quiz"),
    path("question/<int:index>/", views.question_view, name="question"),
    path("result/<int:session_id>/", views.result_view, name="result"),
]

import time
from django.shortcuts import render, redirect, get_object_or_404
from .models import QuizSession, Response
from .utils import QUESTIONS, classify_decision_style


def home(request):
    return render(request, "analyzer/home.html")


def start_quiz(request):
    quiz_session = QuizSession.objects.create()
    request.session["quiz_session_id"] = quiz_session.id
    return redirect("analyzer:question", index=0)


def question_view(request, index):
    quiz_session_id = request.session.get("quiz_session_id")
    if not quiz_session_id:
        return redirect("analyzer:home")

    quiz_session = get_object_or_404(QuizSession, id=quiz_session_id)

    if index >= len(QUESTIONS):
        return redirect("analyzer:result", session_id=quiz_session.id)

    question = QUESTIONS[index]

    if request.method == "POST":
        selected_option = request.POST.get("option")
        start_time = float(request.POST.get("start_time", time.time()))
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        hesitation = response_time > 5

        if selected_option:
            Response.objects.create(
                quiz_session=quiz_session,
                question_text=question["text"],
                selected_option=selected_option,
                response_time=response_time,
                hesitation=hesitation,
            )

        next_index = index + 1
        if next_index < len(QUESTIONS):
            return redirect("analyzer:question", index=next_index)
        return redirect("analyzer:result", session_id=quiz_session.id)

    context = {
        "question": question,
        "index": index,
        "start_time": time.time(),
        "total": len(QUESTIONS),
    }
    return render(request, "analyzer/question.html", context)


def result_view(request, session_id):
    quiz_session = get_object_or_404(QuizSession, id=session_id)
    responses = quiz_session.responses.all()

    if not responses.exists():
        return redirect("analyzer:home")

    avg_response_time = round(
        sum(r.response_time for r in responses) / responses.count(), 2
    )
    total_hesitations = sum(1 for r in responses if r.hesitation)
    decision_style = classify_decision_style(avg_response_time, total_hesitations)

    quiz_session.avg_response_time = avg_response_time
    quiz_session.total_hesitations = total_hesitations
    quiz_session.decision_style = decision_style
    quiz_session.completed = True
    quiz_session.save()

    context = {
        "session": quiz_session,
        "responses": responses,
    }
    return render(request, "analyzer/result.html", context)

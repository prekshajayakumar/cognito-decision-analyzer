import time

from django.shortcuts import render, redirect, get_object_or_404

from .models import QuizSession, Response
from .utils import QUESTIONS, extract_features
from ml.predictor import predict_decision_style


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
        response_time = round(time.time() - start_time, 2)
        hesitation = response_time > 5

        if selected_option:
            Response.objects.create(
                quiz_session=quiz_session,
                question_number=index + 1,
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
        "progress": int(((index + 1) / len(QUESTIONS)) * 100),
    }

    return render(request, "analyzer/question.html", context)


def result_view(request, session_id):
    quiz_session = get_object_or_404(QuizSession, id=session_id)
    responses = list(quiz_session.responses.all().order_by("question_number"))

    if not responses:
        return redirect("analyzer:home")

    features = extract_features(responses)
    predicted_style, confidence_score = predict_decision_style(features)

    quiz_session.avg_response_time = features["avg_response_time"]
    quiz_session.median_response_time = features["median_response_time"]
    quiz_session.max_response_time = features["max_response_time"]
    quiz_session.min_response_time = features["min_response_time"]
    quiz_session.std_response_time = features["std_response_time"]
    quiz_session.total_time = features["total_time"]
    quiz_session.hesitation_count = features["hesitation_count"]
    quiz_session.hesitation_ratio = features["hesitation_ratio"]
    quiz_session.fast_answer_count = features["fast_answer_count"]
    quiz_session.slow_answer_count = features["slow_answer_count"]
    quiz_session.predicted_style = predicted_style
    quiz_session.confidence_score = confidence_score
    quiz_session.completed = True
    quiz_session.save()

    context = {
        "session": quiz_session,
        "responses": responses,
        "response_times": [r.response_time for r in responses],
    }

    return render(request, "analyzer/result.html", context)

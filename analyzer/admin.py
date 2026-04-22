from django.contrib import admin
from .models import QuizSession, Response


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "decision_style",
        "avg_response_time",
        "total_hesitations",
        "completed",
        "created_at",
    )
    list_filter = ("decision_style", "completed", "created_at")
    search_fields = ("decision_style",)
    ordering = ("-created_at",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quiz_session",
        "question_text",
        "selected_option",
        "response_time",
        "hesitation",
        "created_at",
    )
    list_filter = ("hesitation", "created_at")
    search_fields = ("question_text", "selected_option")
    ordering = ("-created_at",)

from django.contrib import admin
from .models import QuizSession, Response


@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "predicted_style",
        "confidence_score",
        "avg_response_time",
        "hesitation_count",
        "completed",
        "created_at",
    )
    list_filter = ("predicted_style", "completed", "created_at")
    search_fields = ("predicted_style",)
    ordering = ("-created_at",)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "quiz_session",
        "question_number",
        "selected_option",
        "response_time",
        "hesitation",
        "created_at",
    )
    list_filter = ("hesitation", "created_at")
    search_fields = ("question_text", "selected_option")
    ordering = ("-created_at",)


admin.site.site_header = "Cognito Admin"
admin.site.site_title = "Cognito Admin Portal"
admin.site.index_title = "Decision Analyzer Dashboard"

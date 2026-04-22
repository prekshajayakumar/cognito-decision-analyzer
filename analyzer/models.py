from django.db import models


class QuizSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    avg_response_time = models.FloatField(null=True, blank=True)
    total_hesitations = models.IntegerField(default=0)
    decision_style = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.decision_style or 'In Progress'}"


class Response(models.Model):
    quiz_session = models.ForeignKey(
        QuizSession, on_delete=models.CASCADE, related_name="responses"
    )
    question_text = models.CharField(max_length=255)
    selected_option = models.CharField(max_length=100)
    response_time = models.FloatField()
    hesitation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question_text} - {self.selected_option}"

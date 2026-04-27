from django.db import models


class QuizSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    avg_response_time = models.FloatField(null=True, blank=True)
    median_response_time = models.FloatField(null=True, blank=True)
    max_response_time = models.FloatField(null=True, blank=True)
    min_response_time = models.FloatField(null=True, blank=True)
    std_response_time = models.FloatField(null=True, blank=True)
    total_time = models.FloatField(null=True, blank=True)

    hesitation_count = models.IntegerField(default=0)
    hesitation_ratio = models.FloatField(default=0)
    fast_answer_count = models.IntegerField(default=0)
    slow_answer_count = models.IntegerField(default=0)

    predicted_style = models.CharField(max_length=50, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.id} - {self.predicted_style or 'In Progress'}"


class Response(models.Model):
    quiz_session = models.ForeignKey(
        QuizSession, on_delete=models.CASCADE, related_name="responses"
    )
    question_number = models.IntegerField(default=0)
    question_text = models.CharField(max_length=255)
    selected_option = models.CharField(max_length=100)
    response_time = models.FloatField()
    hesitation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.question_number}: {self.selected_option}"

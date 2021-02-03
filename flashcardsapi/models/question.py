"""Question model module"""
from django.db import models


class Question(models.Model):
    """Question database model"""
    question_text = models.CharField(max_length=500)
    question_display = models.CharField(max_length=45)
    answer_value = models.CharField(max_length=500)
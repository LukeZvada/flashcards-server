"""CategoryQuestion model module"""
from django.db import models


class CategoryQuestion(models.Model):
    """CategoryQuestion database model"""
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="category_question")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="category_question")
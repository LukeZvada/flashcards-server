"""TopicQuestion model module"""
from django.db import models


class TopicQuestion(models.Model):
    """TopicQuestion database model"""
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE, related_name="topic_question")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="topic_question")
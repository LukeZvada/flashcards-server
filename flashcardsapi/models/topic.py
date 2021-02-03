"""Topic model module"""
from django.db import models


class Topic(models.Model):
    """Topic database model"""
    label = models.CharField(max_length=25)
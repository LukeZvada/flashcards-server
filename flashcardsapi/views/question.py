"""
View module for handling requests for questions
"""

from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from flashcardsapi.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    """  Serializer for questions """
    class Meta:
        model = Question
        fields = ("id", "question_text", "question_display", "answer_value", "approved")


class Questions(ViewSet):
    """ Questions viewset """

    def list(self, request):
        """
        Return all questions
        """

        questions = Question.objects.all()

        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ Return single question """
        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
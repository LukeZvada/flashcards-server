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
from rest_framework.decorators import action

class QuestionSerializer(serializers.ModelSerializer):
    """  Serializer for questions """
    class Meta:
        model = Question
        fields = ("id", "question_text", "question_display", "answer_value", "approved")


class Questions(ViewSet):
    """ Questions viewset """

    def list(self, request):
        """ Return all questions """

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

    def create(self, request):
        """ Allow an admin to create a question """
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            question = Question()
            question.question_text = request.data["question_text"]
            question.question_display = request.data["question_display"]
            question.answer_value = request.data["answer_value"]
            try:
                question.save()
                serializer = QuestionSerializer(question, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not authorized to create a new question."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        """ Allow an admin to edit a question """
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            question = Question.objects.get(pk=pk)
            question.question_text = request.data["question_text"]
            question.question_display = request.data["question_display"]
            question.answer_value = request.data["answer_value"]
            try:
                question.save()
                serializer = QuestionSerializer(question, context={'request': request})
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not authorized to make changes to this resource."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        """ Allow an admin to delete a question """
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            try:
                question = Question.objects.get(pk=pk)
                question.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Question.DoesNotExist:
                return Response({"reason": "Question does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not authorized to delete this resource"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['PUT'], detail=True)
    def change_question_approved_status(self, request, pk=None):
        """ Allows an admin to change the approved field on a question """
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            question = Question.objects.get(pk=pk)
            # sets the boolean value to the oppostie of what is being sent from the client
            question.approved = not request.data["approved"] 
            question.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "You are not authorized."}, status=status.HTTP_401_UNAUTHORIZED)


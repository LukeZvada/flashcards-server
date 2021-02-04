"""CategoryQuestions Views Module"""
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from flashcardsapi.models import Category, CategoryQuestion, Question


class CategoryQuestions(ViewSet):
    """ Responsible for GET, POST, DELETE """

    def list(self, request):
        """ GET all categoryquestion objects """
        categoryquestions = CategoryQuestion.objects.all()

        category_id = self.request.query_params.get("categoryId", None)
        if category_id is not None:
            categoryquestions = categoryquestions.filter(category_id=category_id)

        serializer = CategoryQuestionSerializer(
            categoryquestions, many=True, context={'request', request})
        return Response(serializer.data)

    def create(self, request):
        """ POST """
        categoryquestion = CategoryQuestion()

        question_id = request.data["question_id"]
        category_id = request.data["category_id"]

        # check if question exists
        try:
            question = Question.objects.get(id=question_id)

        except Question.DoesNotExist:
            return Response({'message: invalid post id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # check if category exists
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'message: invalid reaction id'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # check if categoryquestion exists

        try:
            categoryquestion = CategoryQuestion.objects.get(
                question=question, category=category)
        except CategoryQuestion.DoesNotExist:
        #     #if it does not exist, make new obj
            
            categoryquestion = CategoryQuestion()
            categoryquestion.category = category
            categoryquestion.question = question
         

        try:
            categoryquestion.save()
            serializer = CategoryQuestionSerializer(
                categoryquestion, many=False, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """ DELETE """
        try:
            categoryquestion = CategoryQuestion.objects.get(pk=pk)
            categoryquestion.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except CategoryQuestion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryQuestionSerializer(serializers.ModelSerializer):
    """ Serializes CategoryQuestions """
    class Meta:
        model = CategoryQuestion
        fields = ('id', 'category', 'question')
        depth = 1
       

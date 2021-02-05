"""View module for category requests"""
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from flashcardsapi.models import Category
from rest_framework.decorators import action

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "label", "approved")

class Categories(ViewSet):
    def create(self, request):
        """POST operations for categories by admins only"""
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            category = Category()
            category.label = request.data["label"]
            try:
                category.save()
                serializer = CategorySerializer(category, context={'request' : request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "Only admins can create a category"},
                status=status.HTTP_401_UNAUTHORIZED
                )

    def list(self, request):
        """Return all categories"""
        categories = Category.objects.all()
        #GET /categories?cat={search}
        search = self.request.query_params.get('cat', None)
        if search is not None:
            categories = Category.objects.filter(Q(label__contains=search))

        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve single category specifically requested
        in Ticket #23 with a 'def retrieve ???' so it seemed like this was definately needed """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'message' : "***BUZZER NOISE***, doesn't exist, try again"},
            status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """DELETE a category but only allowed by admins"""
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            try:
                category = Category.objects.get(pk=pk)
                category.delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({"reason": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Stop, seriously, just stop. You are not an admin'},
            status=status.HTTP_403_FORBIDDEN)
        
    def update(self, request, pk=None):
        """Update operation for a category by admins only"""
        current_user = User.objects.get(id=request.user.id)
        if current_user.is_staff:
            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                return Response({"reason": "Doesn't Exist"}, status=status.HTTP_400_BAD_REQUEST)
            category.label = request.data['label']
            category.approved = False
            try:
                category.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': "*Sigh*, you're not changing a thing, non-admin"},
            status=status.HTTP_403_FORBIDDEN)

    @action(methods=['patch'], detail=True)
    def approve(self, request, pk=None):
        if request.method == "PATCH":
            current_user = User.objects.get(id=request.user.id)
            if current_user.is_staff:
                category = Category.objects.get(pk=pk)
                category.approved = request.data['approved']
                category.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': "And I would do anything for love, but I won't do that (bc you're not an admin)"},
                status=status.HTTP_403_FORBIDDEN)
                

            

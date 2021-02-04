""" CurrentUser ViewSet Module"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action


class CurrentUser(ViewSet):
    """User Class"""

    def list(self, request):
        """ handles GET currently logged in user """

        #the code in the parentheses is like a WHERE clause in SQL
        user = request.auth.user

        #imported the UserSerializer from rareuser.py to use in this module
        serializer = UserSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)

    @action(methods=['PUT'], detail=True)
    def approve(self, request, pk=None):

        user = User.objects.get(pk=pk)

        if user.is_staff != False:
            user.is_staff = True
            user.save()
        
        elif user.is_staff != True:
            user.is_staff = False
            user.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """Serializer """

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')
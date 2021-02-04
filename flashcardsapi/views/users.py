"""User viewset and serializer"""
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for User"""
    class Meta:
        model = User
        fields= ('id', 'username', 'is_staff')

class UserViewSet(ModelViewSet):

    def list(self, request):
        # queryset = self.get_queryset()
        queryset = User.objects.get(id=request.user.id)
        
        serializer_class = UserSerializer(queryset, many=False)
        return Response(serializer_class.data)
    
    @action(methods=['PUT'], detail=True)
    def flip_is_staff(self, request, pk=None):

        user = User.objects.get(pk=pk)

        if user.is_staff == True:
            user.is_staff = False
            user.save()
        else:
            user.is_staff = True
            user.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
  

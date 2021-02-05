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


class Questions(ViewSet):
    """ Questions viewset """

    def list(self, request):
        """
        Handles GET requests to the /questions resource
        Method arguments:
            request -- The full HTTP request object
        URL: http://localhost:8000/questions
        Request Method: GET
        Response:
            {
                "id": 1,

            }
        """
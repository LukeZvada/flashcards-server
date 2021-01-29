"""
View module for handling user authentication and new user registration
"""
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token

@csrf_exempt
def register(request):
    '''
    Handles the registration of a new user, and authentication
    Method arguments:
        request -- The full HTTP request object
    URL: http://localhost:8000/register
    Request Method: POST
    Body:
        {
        "username": "harrypotter",
        "email": "harry@potter.com",
        "password": "harry",
        "first_name": "Harry",
        "last_name": "Potter"
        }
    Response:
        {
        "token": "50475b0889f3e433c467ad0afb20fe68b15d9c0c"
        }
    Body:
        {
        "username": "hermionegranger",
        "email": "hermione@granger.com",
        "password": "harry",
        "first_name": "Hermione",
        "last_name": "Granger"
        }
    Response:
        {
        "token": "d9f9daa316324df9460755af022a2c087946b606"
        }
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Create a new user by invoking the `create_user` helper method on Django's built-in User model
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name'],
        is_active=True,
        is_staff=False
    )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)

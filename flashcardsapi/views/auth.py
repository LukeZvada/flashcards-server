"""
View module for handling user authentication and new user registration
"""
import json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@csrf_exempt
def register(request):
    '''
    Handles the registration of a new user
    Method arguments:
        request -- The full HTTP request object
    URL: http://localhost:8000/register
    Request Method: POST
    Body (admin):
        {
        "username": "harrypotter",
        "email": "harry@potter.com",
        "password": "harry",
        "first_name": "Harry",
        "last_name": "Potter"
        }
    Response:
        {
        "token": "e48584ea29993d6e7b6fc97da6e29ab1c24ef1e7"
        }
    Body (not-admin):
        {
        "username": "hermionegranger",
        "email": "hermione@granger.com",
        "password": "harry",
        "first_name": "Hermione",
        "last_name": "Granger"
        }
    Response:
        {
        "token": "079ef37acfa281ee45cbebb5199728940b4b4194"
        }
    '''

    # Load JSON string of request body into a dict
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


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a gamer

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')
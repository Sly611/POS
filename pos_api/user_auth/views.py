
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
# from serializer import CustomUserSerializer
from rest_framework.status import *
from .schema import register_user_schema
from .serializer import *

# Create your views here.

class RegisterSuperUserView(APIView):
    """
    Handles super_user registration.

    This view allows a super_user to register by providing their details.
    The details are validated and saved if valid.

    Methods:
        post(request): Handles POST requests to register a super user.

    Args:
        request (Request): The request object containing user data.

    Returns:
        Response: The response object containing serialized user data 
                  and HTTP 201 status code if successful, or 
                  HTTP 400 status code if validation fails.
    """
    @register_user_schema
    def post(self, request):
        serializer = CreateSuperUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class RegisterUserView(APIView):

    """
    Handles user registration.

    This view allows new users to register by providing their details.
    The details are validated and saved if valid.

    Methods:
        post(request): Handles POST requests to register a new user.

    Args:
        request (Request): The request object containing user data.

    Returns:
        Response: The response object containing serialized user data 
                  and HTTP 201 status code if successful, or 
                  HTTP 400 status code if validation fails.
    """
    @register_user_schema
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user authentication and login.

    This view allows users to log in by providing their username and password.
    Upon successful authentication, the user is logged in.

    Methods:
        post(request): Handles POST requests to log in a user.

    Args:
        request (Request): The request object containing username and password.

    Returns:
        Response: The response object with a success message and 
                  HTTP 200 status code if login is successful, 
                  HTTP 401 status code if authentication fails, or 
                  HTTP 400 status code if required data is missing.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is not None and password is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'login successful'}, status=HTTP_200_OK)
            else:
                return Response({'message': 'invalid username or password'}, status=HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'provide username and password'}, status=HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Handles user logout.

    This view logs out the currently authenticated user.

    Methods:
        post(request): Handles POST requests to log out the user.

    Args:
        request (Request): The request object.

    Returns:
        Response: The response object with a success message and 
                  HTTP 200 status code if logout is successful.
    """
    def post(self, resquest):
        logout(resquest)
        return Response({'message': 'logged out successfully'}, status=HTTP_200_OK)
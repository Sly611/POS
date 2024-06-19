
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
# from serializer import CustomUserSerializer
from rest_framework.status import *

from .serializer import CustomUserSerializer


# Create your views here.


class UserCreateView(APIView):

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):

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


class UserLogoutView(APIView):
    def post(self, resquest):
        logout(resquest)
        return Response({'message': 'logged out successfully'}, status=HTTP_200_OK)
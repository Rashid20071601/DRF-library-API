from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import *

class UserLoginAPIView(APIView):
    '''
    API-представление для входа пользователя
    '''
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)


class UserRegisterAPIView(APIView):
    '''
    API-представление для регистрации пользователя
    '''
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializers = UserRegisterSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
                {
                    'detail': 'Пользователь успешно зарегистрирован',
                    'token': token.key
                },
                status=status.HTTP_201_CREATED
            )
    

class UserLogoutAPIView(APIView):
    '''
    API-представление для выхода пользователя
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response({'detail': 'Вы успешно вышли из аккаунта'}, status=status.HTTP_200_OK)
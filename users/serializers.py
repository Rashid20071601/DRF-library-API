from rest_framework import serializers
from django.contrib.auth.models import User


class UserLoginSerializer(serializers.Serializer):
    '''
    Сериализатор для аутентификации пользователя.
    '''
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserRegisterSerializer(serializers.Serializer):
    '''
    Сериализатор для регистрации пользователя.
    '''
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    # Проверяем уникальность имени пользователя
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже существует!')
        return value

    # Проверяем пароли на совпадение
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs
    
    # Создаем пользователя
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        user = User.objects.create_user(username=username, password=password)
        return user
        

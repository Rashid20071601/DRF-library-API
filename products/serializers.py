from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializer для работы с моделью Product
    '''
    class Meta:
        '''
        Метаданные сериализатора
        '''
        model = Product
        fields = '__all__'

    # Метод для валидации поля 'price'
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Цена должна быть положительной')
        return value

    # Метод для валидации поля 'name'
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название должно быть заполнено')
        return value
    
    # Метод для валидации поля 'description'
    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError('Описание должно быть заполнено')
        return value
            
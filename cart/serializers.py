from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer
from products.models import Product



class CartItemSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор, только для чтения (GET-запросы)
    product = ProductSerializer(read_only=True)

    # Поле product_id — для создания и удаления (POST-запросы)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


    def validate_quantity(self, value):
        # Проверка: количество должно быть больше 0
        if value <= 0:
            raise serializers.ValidationError("Количество товаров должно быть больше 0.")
        return value


    def create(self, validated_data):
        # Получаем пользователя из запроса
        user = self.context['request'].user
        product = validated_data.pop('product_id')
        quantity = validated_data.pop('quantity', 1)

        # Обновляем количество, если товар уже есть в корзине
        cart_item, created = CartItem.objects.update_or_create(
            user=user, product=product, defaults={'quantity': quantity}
        )

        if not created:
            # Увеличиваем количество, если товар уже был
            cart_item.quantity += quantity
            cart_item.full_clean()  # Проверка модели
            cart_item.save()

        return cart_item
    

    def validate_product_id(self, value):
        # Проверка: товар должен быть доступен
        if not Product.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Товар с таким ID не существует.")
        return value
    

    def validate_quantity(self, value):
        if value > 100:
            raise serializers.ValidationError("Количество товаров не должно превышать 100.")
        return value
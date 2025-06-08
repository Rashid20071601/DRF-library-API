from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CartItem
from .serializers import CartItemSerializer


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Товар успешно добавлен в корзину!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        try:
            cart_item = CartItem.objects.get(user=user, product=product_id)
        except CartItem.DoesNotExist:
            return Response({'message': 'Товар не найден в корзине!'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Товар удален из корзины!'}, status=status.HTTP_200_OK)
        
        cart_item.full_clean()
        cart_item.save()
        return Response({'message': 'Количество товара в корзине обновлено!'}, status=status.HTTP_200_OK)
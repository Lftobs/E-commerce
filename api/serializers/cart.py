from rest_framework import serializers
from store.models.cart import Cart, CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        extra_kwargs = {'cart': {'read_only': True}, 'id': {'read_only': True}}
        

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        extra_kwargs = {'cart': {'read_only': True}, 'id': {'read_only': True}}

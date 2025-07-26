from rest_framework import serializers

from store.models.order import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}, 'total_price': {'read_only': True}}
        # extra_kwargs = {'created_at': {'read_only': True}, 'updated_at': {'read_only': True}}

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
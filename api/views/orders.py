from django.http import Http404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from api.serializers.order import OrderSerializer, OrderItemSerializer
from api.utils.helpers import res_gen
from store.models.cart import Cart
from store.models.order import Order


class OrderViewset(viewsets.ModelViewSet):
    model = Order
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        try:
            return Order.objects.filter(user=self.request.user)
        except Order.DoesNotExist:
            raise Http404("No order found for the user.")
    
    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(profile__user=request.user)
        if cart.cart_items.first() is None:
            return Response({'details': 'Order creation failed because cart is empty!'}, status=status.HTTP_400_BAD_REQUEST)
        order = self.model.objects.create(user=request.user)
        for item in cart.cart_items.all():
            if item.product.stock < item.quantity:
                return Response(
                    {'details': f'Order creation failed because {item.product.name} is out of stock or requested quantity of product is more than the available stock!'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                item.product.stock -= item.quantity
                item.product.save()
            order_item = OrderItemSerializer(data={
                'order': order.pk,
                'product': item.product.pk,
                'quantity': item.quantity,
                'total_price': item.total_price
            })
            if order_item.is_valid():
                order_item.save()
            else:
                return Response(order_item.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order.total_price = order.total_items_price
        order.save()
        cart.cart_items.all().delete()
        res = res_gen(self.serializer_class(order, many=False).data, status.HTTP_201_CREATED, "Order for user cart items create.")
        return Response(res, status=status.HTTP_201_CREATED)

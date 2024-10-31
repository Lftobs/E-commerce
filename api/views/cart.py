from rest_framework import viewsets, permissions

from api.serializers.cart import CartItemSerializer
from store.models.cart import Cart, CartItem


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return self.queryset.filter(cart=cart)
    
    # def perform_create(self, serializer):
    #     cart = Cart.objects.get(user=self.request.user)
    #     product = serializer.validated_data['product']
    #     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    #     if not created:
    #         cart_item.quantity += serializer.validated_data['quantity']
    #         cart_item.save()
    #     else:
    #         serializer.save(cart=cart)

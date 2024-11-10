from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.serializers.cart import CartItemSerializer, CartSerializer
from store.models.cart import Cart, CartItem
from rest_framework.decorators import action


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    model = CartItem
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return cart.cart_items.all()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            cart = Cart.objects.get(user=request.user)
            if cart is None:
                return Response({'detail': 'Cart not found for user'}, status=status.HTTP_404_NOT_FOUND)
            product = serializer.validated_data.get('product')
            existing_product = CartItem.objects.filter(cart=cart, product=product).first()
            if existing_product is not None:
                existing_product.quantity += serializer.validated_data.get('quantity')
                existing_product.save()
                new_serializer = self.serializer_class(existing_product, many=False)
                return Response({'detail': 'Item already in cart so quantity was updated instead', 'data': new_serializer.data}, status=status.HTTP_200_OK)
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='info', url_name='cart-info')
    def cart_info(self, request):
        """ func for cart info endpoint"""
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart, many=False)
        return Response(
            {
                
                'cart_info': serializer.data,
                'cart_items':  self.serializer_class(cart.cart_items, many=True).data,
                'total_cart_items_price': cart.total_price 
                
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='clear-cart', url_name='clear-cart')
    def clear_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart).delete()
        return Response({'detail': 'Cart cleared successfully'}, status=status.HTTP_204_NO_CONTENT)

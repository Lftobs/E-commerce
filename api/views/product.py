from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers.product import ProductSerializer
from store.models.product import Product
from store.models.user import CustomUser
from ..serializers.user import UserListSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import  CreateAPIView, GenericAPIView, ListCreateAPIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow sellers to access certain views.
    Methods
    """
    def  has_permission(self, request, view) -> bool:
         
        return request.user.is_buyer()

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_buyer()
class ProductCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_class = [AllowAny]
        else:
            permission_class=[IsAuthenticated, IsSeller]
        return [permission() for permission in permission_class]

class ProductUpdateDeleteView(GenericAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        product = self.get_queryset(pk)
        if product is None:
            return Response({
                "details": "Product with this id not found"
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(product, many=False)
        return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self, request, pk):
        product = self.get_queryset(pk)
        
        if product is None:
            return Response({
                "details": "Product with this id not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        if product.seller != request.user:
            return Response({
                "details": "You do not  have permission to update this product"
            }, status=status.HTTP_401_UNAUTHORIZED)
        # request.data['seller'] = request.user.id
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    
    def delete(self, request, pk):
        product = self.get_queryset(pk)

        if product is None:
            return Response({
                "details": "Product with this id not found"
            }, status=status.HTTP_404_NOT_FOUND)

        if product.seller != request.user:
            return Response({
                "details": "You do not have permission to delete this product"
            }, status=status.HTTP_401_UNAUTHORIZED)

        product.delete()
        return Response({
            "details": "Product deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)
    
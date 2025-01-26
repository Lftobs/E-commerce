from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers.product import ProductSerializer
from api.utils.helpers import res_gen
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
         
        return request.user.is_seller()

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_seller()
class ProductCreateView(ListCreateAPIView):
    """
    ProductCreateView handles the creation and listing of products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_class = [AllowAny]
        else:
            permission_class=[IsAuthenticated, IsSeller]
        return [permission() for permission in permission_class]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            res = res_gen(serializer.data, status.HTTP_201_CREATED, "Product created successfully")
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductUpdateDeleteView(GenericAPIView):
    """
    ProductUpdateDeleteView handles the retrieval, update, and deletion of a product instance.
    Methods:
        get_queryset(pk): Retrieves a product instance by its primary key.
        get(request, pk): Retrieves and returns a product instance.
        patch(request, pk): Updates a product instance partially.
        delete(request, pk): Deletes a product instance.
    """
    
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
                "message": "Product with this id not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(product, many=False)
        res = res_gen(serializer.data, status.HTTP_200_OK, "Product retrieved successfully")
        return Response(res, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        product = self.get_queryset(pk)
        
        if product is None:
            return Response({
                "message": "Product with this id not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        
        if product.seller != request.user:
            return Response({
                "message": "You do not have permission to update this product",
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = res_gen(serializer.data, status.HTTP_200_OK, "Product updated successfully")
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    
    def delete(self, request, pk):
        product = self.get_queryset(pk)

        if product is None:
            return Response({
                "message": "Product with this id not found",
                "status": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        if product.seller != request.user:
            return Response({
                "message": "You do not have permission to delete this product",
                "status": status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)

        product.delete()
        return Response({
            "message": "Product deleted successfully",
            "status": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)
    
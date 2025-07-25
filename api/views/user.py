from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers
from django.db import transaction
from api.serializers.cart import CartSerializer
from store.models.cart import Cart
from store.models.user import CustomUser
from ..serializers.user import SellerProfileSerializer, UserListSerializer, UserLoginSerializer, UserProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils.helpers import res_gen

 
@api_view(['GET'])
def get_all_users(request):
    if request.query_params:
        user = CustomUser.objects.filter(**request.query_params.dict())
    else:
        user = CustomUser.objects.all()

    if user:
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    
    def get(self, request):
        serializer = self.serializer_class(request.user, many=False)
        return Response(serializer.data)
    
    def put(self, request):
        user = CustomUser.objects.get(email=request.user.email)
        user.email = request.data.get('email')
        user.user_type = request.data.get('user_type')
        user.save()
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SignUp(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
        data = request.data.copy()
        data.update({'password': make_password(data.get('password'))})
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            
            with transaction.atomic():
                user = serializer.save()

                if user.is_seller():
                    print('creating seller profile')
                    profile_serializer = SellerProfileSerializer(data={'user': user.id, "is_seller": True})
                    profile_serializer.is_valid(raise_exception=True)
                    profile = profile_serializer.save()
                else:
                    print('creating buyer profile')
                    profile_serializer = UserProfileSerializer(data={'user': user.id, "is_seller": False})
                    profile_serializer.is_valid(raise_exception=True)
                    profile = profile_serializer.save()

                cart = Cart.objects.create(profile=profile)
                profile.user_cart = cart
                profile.save()

                if user.is_seller():
                    res = res_gen(serializer.data, status.HTTP_201_CREATED, 'Seller account created successfully')
                    return Response(res, status=status.HTTP_201_CREATED)

                res = res_gen(serializer.data, status.HTTP_201_CREATED, 'User created successfully')
                return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    
class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = RefreshToken.for_user(user)

        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        res = res_gen(data, status.HTTP_200_OK, 'User logged in successfully')
        return Response(res, status=status.HTTP_200_OK)

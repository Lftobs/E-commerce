from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models.user import CustomUser
from ..serializers.user import UserListSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import  CreateAPIView, GenericAPIView 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
 
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
    
class SignUp(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def post(self, request):
        data = request.data.copy()
        data.update({'password': make_password(data.get('password'))})
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    
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
        return Response(data, status=status.HTTP_200_OK)
    
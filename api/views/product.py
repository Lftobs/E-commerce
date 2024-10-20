from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models.user import CustomUser
from ..serializers.user import UserListSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import  CreateAPIView, GenericAPIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
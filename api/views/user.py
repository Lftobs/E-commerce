from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from user.models.user import CustomUser
from ..serializers.user import UserSerializer
 
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
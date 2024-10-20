from rest_framework import serializers
from store.models.user import CustomUser
from django.contrib.auth import authenticate
 
class UserSerializer(serializers.ModelSerializer):
    """ Serializer class to create users """
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
class UserListSerializer(serializers.ModelSerializer):
    """ Serializer class to list and users """
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'user_type')
        
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with email and password.
    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
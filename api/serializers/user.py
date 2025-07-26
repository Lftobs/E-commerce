from rest_framework import serializers
from store.models.user import BusinessProfile, CustomUser, SellerProfile, UserProfile
from django.contrib.auth import authenticate
 
class UserSerializer(serializers.ModelSerializer):
    """ Serializer class to create users """
    class Meta:
        model = CustomUser
        fields = ('email', 'user_type', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer class to create user profile """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = UserProfile
        fields = ('user', 'first_name', 'last_name', 'phone_number', 'address', 'is_seller')
        extra_kwargs = {
            'is_seller': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False},
        }
        
class SellerProfileSerializer(serializers.ModelSerializer):
    """ Serializer class to create seller profile """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    class Meta:
        model = SellerProfile
        fields = ('user', 'first_name', 'last_name', 'phone_number', 'address', 'is_seller')
        extra_kwargs = {'is_seller': {'required': True}}

class BusinessProfileSerializer(serializers.ModelSerializer):
    """ Serializer class to create business profile for sellers """
    class Meta:
        model = BusinessProfile
        fields = ('business_name', 'business_address', 'business_phone_number', 'business_email')
        extra_kwargs = {
            'business_name': {'required': True},
            'business_address': {'required': True},
            'business_phone_number': {'required': True},
            'business_email': {'required': True}
        }
        
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

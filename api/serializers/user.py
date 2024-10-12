from django.db.models import fields
from rest_framework import serializers
from user.models.user import CustomUser
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'user_type')
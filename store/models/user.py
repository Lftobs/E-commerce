from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from ..managers import CustomUserManager
from uuid_extensions import uuid7
from django.db.models import UUIDField


class CustomUser(AbstractUser):
    """Custom user model with email as username"""
    use_in_migrations = True
    username = None
    id = UUIDField(primary_key=True, default=uuid7(), editable=False)
    email = models.EmailField(_("email address"), unique=True)
    custom_groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
    )

    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][0])
    user_profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_buyer(self):
        """Check if the user is a buyer."""
        return self.user_type == 'buyer'

    def is_seller(self):
        """Check if the user is a seller."""
        return self.user_type == 'seller'

    def is_admin(self):
        """Check if the user is an admin."""
        return self.user_type == 'admin'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
 
    class Meta:
        db_table = 'custom_user'
        app_label = 'store'


class UserProfile(models.Model):
    """User profile model"""
    id = UUIDField(primary_key=True, default=uuid7(), editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_seller = models.BooleanField(default=False)

    user_cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
    
    def is_seller_profile(self):
        """Check if the user profile is a seller profile."""
        return hasattr(self, 'seller_profile')

    class Meta:
        db_table = 'user_profile'
        app_label = 'store'

class SellerProfile(UserProfile):
    """Seller profile model"""
    business_profile = models.OneToOneField('BusinessProfile', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'seller_profile'
        app_label = 'store'
        
class BusinessProfile(models.Model):
    """Business profile model for sellers"""
    id = UUIDField(primary_key=True, default=uuid7(), editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    business_phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Business Profile of {self.user.email}"

    class Meta:
        db_table = 'business_profile'
        app_label = 'store'
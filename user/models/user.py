from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from ..managers import CustomUserManager


class CustomUser(AbstractUser):
    """Custom user model with email as username"""
    use_in_migrations = True
    username = None
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
    user_cart = models.OneToOneField('Cart', on_delete=models.CASCADE, null=True, blank=True)

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
        app_label = 'user'


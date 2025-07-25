from django.db import models
from uuid_extensions import uuid7
from .user import CustomUser

class Product(models.Model):
    """Product model"""
    def upload_to(instance, filename):
        return '/'.join(['products', str(instance.seller), filename])
    id = models.UUIDField(primary_key=True, default=uuid7(), editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload_to, blank=True)
    stock = models.PositiveIntegerField() # number of items available
    seller = models.ForeignKey(CustomUser, related_name='prod', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        app_label = 'store'

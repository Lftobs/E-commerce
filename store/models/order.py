from django.db import models

from .product import Product
import string
import random

from .user import CustomUser

class Order(models.Model):
    """
    Order model represents a customer's order in the e-commerce system.
    Properties:
        total_price (float): Calculates the total price of all items in the order.
    Methods:
        __str__(): Returns a string representation of the order.
    """
    Order_Status = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    tracking_id = models.CharField(unique=True, max_length=15, editable=False)
    status = models.CharField(max_length=60, choices=Order_Status, default=Order_Status[0][0])
    total_price = models.DecimalField(max_digits=100000000, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def generate_tracking_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    
    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = self.generate_tracking_id()
        super().save(*args, **kwargs)
    
    @property
    def total_items_price(self):
        items = self.order_items.all()
        return sum(item.total_price for item in items)

    def __str__(self):
        return f"Order for {self.user.email}"
    
    class Meta:
        db_table ='order'


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=100000000, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"

    class Meta:
        db_table = 'order_item'
        app_label = 'store'
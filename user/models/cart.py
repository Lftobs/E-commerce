from django.db import models
from .user import CustomUser 
from .product import Product


class Cart(models.Model):
    """Cart model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # items = models.ManyToManyField('CartItem', related_name='cart_items', blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart for {self.user.email}"
 
    class Meta:
        db_table = 'cart'
        app_label = 'user'
        
class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart item for {self.cart.user.email}"

    class Meta:
        db_table = 'cart_item'
        app_label = 'user'
from django.contrib import admin

from .models.cart import Cart, CartItem
from .models.product import Product
from .models.user import BusinessProfile, CustomUser, SellerProfile, UserProfile
from .models.order import Order
# from .models import User


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(SellerProfile)
admin.site.register(UserProfile)
admin.site.register(BusinessProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Order)

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.orders import OrderViewset
from .views import home, user, product
from .views.cart import CartItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cartitems')
router.register(r'order', OrderViewset, basename='order')

urlpatterns = [
    path('', home.ApiOverview, name='home'),
    # auth/users
    path('auth/users/all/', user.get_all_users, name='list-users'),
    path('auth/user/', user.UserView.as_view(), name='user-edit-and-retrieve'),
    path('auth/signup/', user.SignUp.as_view(), name='signup-user'),
    path("auth/login/", user.UserLoginAPIView.as_view(), name="login-user"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # products
    path('product/', product.ProductListView.as_view(), name='list-products'),
    path('product/<str:pk>/', product.ProductDetailView.as_view(), name='product-detail'),

    # product inventory
    path('inventory/', product.ProductInventoryCreateView.as_view(), name="create-and-list-product"),
    path('inventory/<str:pk>', product.ProductInventoryUpdateDeleteView.as_view(), name="update-delete-product")
]

urlpatterns += router.urls
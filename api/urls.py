from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import home, user, product
from .views.cart import CartItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cartitems')

urlpatterns = [
    path('', home.ApiOverview, name='home'),
    # auth/users
    path('users/all/', user.get_all_users, name='list-users'),
    path('user/', user.UserView.as_view(), name='user-edit-and-retrieve'),
    path('signup/', user.SignUp.as_view(), name='signup-user'),
    path("login/", user.UserLoginAPIView.as_view(), name="login-user"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # products
    path('product/', product.ProductCreateView.as_view(), name="create-and-list-product"),
    path('product/<int:pk>', product.ProductUpdateDeleteView.as_view(), name="update-delete-product")
]

urlpatterns += router.urls
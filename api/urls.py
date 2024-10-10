from django.contrib import admin
from django.urls import path, include

from .views import home, user

urlpatterns = [
    path('', home.ApiOverview, name='home'),
    path('users/all/', user.get_all_users, name='list-users'),
]
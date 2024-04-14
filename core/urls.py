from django.urls import path
from . import views
from .views import (
    ItemDetailView,
    checkout,
    HomeView,
    login_register,
    add_to_cart,
    remove_from_cart,
    logout_user,
    register
)


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product_details/<slug>/', ItemDetailView.as_view(), name='product_details'),
    path('checkout/',checkout, name='checkout'),
    path('login-register.html', views.login_register, name='login-register'),
    path('logout_user', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    ]
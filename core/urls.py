from django.urls import path
from .views import products 

app_name = 'core'

urlpatterns = [
    path('',products, name='products'),
    ]
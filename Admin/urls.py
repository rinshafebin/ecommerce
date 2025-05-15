from django.urls import path
from Admin.views import ProductlistApi

urlpatterns = [
    path('products/',ProductlistApi.as_view(),name='product-list'),
    
]

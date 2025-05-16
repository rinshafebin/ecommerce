from django.urls import path
from Admin.views import ProductlistApi,ProductCreateApi,ProductUpdateApi,ViewProductsByCategory,ProductDeleteApi

urlpatterns = [
    path('allproducts/',ProductlistApi.as_view(),name='allproducts'),
    path('createproduct/',ProductCreateApi.as_view(),name='createproduct'),
    path('updateproduct/',ProductUpdateApi.as_view(),name='updateproduct'),
    path('productsbycategory/',ViewProductsByCategory.as_view(),name='categoryview'),
    path('productdelete/',ProductDeleteApi.as_view(),name='deleteproduct'),
    
]

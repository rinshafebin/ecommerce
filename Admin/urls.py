from django.urls import path
from Admin.views import ProductlistApi,ProductCreateApi,ProductUpdateApi,ViewProductsByCategory,ProductDeleteApi

urlpatterns = [
    path('all_products/',ProductlistApi.as_view(),name='allproducts'),
    path('create_product/',ProductCreateApi.as_view(),name='create_product'),
    path('update_product/',ProductUpdateApi.as_view(),name='update_product'),
    path('productsbycategory/',ViewProductsByCategory.as_view(),name='category_view'),
    path('product_delete/',ProductDeleteApi.as_view(),name='delete_product'),
    
]

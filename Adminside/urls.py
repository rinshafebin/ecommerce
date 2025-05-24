from django.urls import path
from Adminside.views import ViewAllUsers,Products,ProductDetails,ViewProductsByCategory,UserDetail

urlpatterns = [
    path('allusers/',ViewAllUsers.as_view(),name='allusers'),
    path('userdetail/<int:pk>/',UserDetail.as_view(),name='userdetail'),
    
    path('products/',Products.as_view(),name='products'),
    path('createproducts/',Products.as_view(),name='createproducts'),
   
    path('getproduct/<int:pk>/',ProductDetails.as_view(),name='productdetail'),
    path('updateproduct/<int:pk>/',ProductDetails.as_view(),name='updateproduct'),
    path('deleteproduct/<int:pk>/',Products.as_view(),name='deleteproduct'),
    path('productbycategory/<str:category>/',ViewProductsByCategory.as_view(),name='productdetailbycategory'),

  
]

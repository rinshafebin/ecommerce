from django.urls import path
from AdminUser.views import ViewAllUsers,Products
urlpatterns = [
    path('allusers/',ViewAllUsers.as_view(),name='allusers'),
    path('userdetail/<int:pk>/',ViewAllUsers.as_view(),name='userdetail'),
    path('products/',Products.as_view(),name='products'),
    path('createproduct/',Products.as_view(),name='products'),


    
]

from django.urls import path
from Admin.views import ViewAllUsers,ViewSpecificUser,Productlist,ProductCreate,ProductUpdate,ViewProductsByCategory,ProductDelete,ViewProduct

urlpatterns = [
    path('allusers/',ViewAllUsers.as_view(),name='allusers'),
    path('viewuser/<int:pk>/',ViewSpecificUser.as_view(),name='userdetail'),

    path('allproducts/',Productlist.as_view(),name='allproducts'),
    path('createproduct/',ProductCreate.as_view(),name='createproduct'),
    path('viewproduct/<int:pk>/',ViewProduct.as_view(),name='allusers'),
    path('updateproduct/<int:pk>/',ProductUpdate.as_view(),name='updateproduct'),
    path('productsbycategory/<str:category>/',ViewProductsByCategory.as_view(),name='categoryview'),
    path('productdelete/<int:pk>/',ProductDelete.as_view(),name='deleteproduct'),
    
]

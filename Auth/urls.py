from django.urls import path
from Auth.views import UserRegistration,Login,Logout,ChangePassword,EmailVerify

urlpatterns = [
    path('usersignup/',UserRegistration.as_view(),name='usersignup'),  
    path('emailverify/<uidb64>/<token>/',EmailVerify.as_view(),name='emailverify'),
    path('login/',Login.as_view(),name='login'),
    path('changepassword/',ChangePassword.as_view(),name='changepassword'), 
    path('logout/',Logout.as_view(),name='logout') 
    
]

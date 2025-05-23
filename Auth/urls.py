from django.urls import path
from Auth.views import UserRegistration,Login,Logout,ChangePassword,EmailVerify,ResetPassword,ResetPasswordview

urlpatterns = [
    path('usersignup/',UserRegistration.as_view(),name='usersignup'),  
    path('emailverify/<uidb64>/<token>/',EmailVerify.as_view(),name='emailverify'),
    path('login/',Login.as_view(),name='login'),
    path('changepassword/',ChangePassword.as_view(),name='changepassword'), 
    path('resetpassword/',ResetPassword.as_view(),name='resetpassword'), 
    path('resetpassword/<uidb64>/<token>/',ResetPasswordview.as_view(),name='resetpassword'), 
    path('logout/',Logout.as_view(),name='logout') ,
    
]

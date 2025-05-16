from django.urls import path
from Authentication.views import UserRegistrationApi

urlpatterns = [
    path('user_signup/',UserRegistrationApi.as_view(),name='user_signup'),    
]

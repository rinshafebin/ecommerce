from rest_framework.views import APIView
from Auth.serializers import UserRegistrationSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
# --------------------------  registration  -------------------------------------------

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            password = validated_data['password']
            validated_data['password'] = make_password(password)   
            user = CustomUser.objects.create(**validated_data) 
            user.is_active = False
            user.save()  
            
            
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk)) 
            token = default_token_generator.make_token(user)
            verification_link = f"http://{current_site.domain}{reverse('email_verify', kwargs={'uidb64':uid,'token':token})}
            
            subject = 'Activate Your Account'
            message = f'hi{user.username},\nPlease click the link below to verify your email and activate your account : \n{verification_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject,message,from_email,recipient_list,fail_sliently = False)

            
                                                        
            return Response({'message':'user created succesfully ,please check your mail to verify your account'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
# -------------------------- Login  -------------------------------------------
   
class Login(APIView):
    def post(self,request):
        serilaizer = LoginSerializer(data=request.data)
        if serilaizer.is_valid():
            user = serilaizer.validated_data['user']
            refresh = RefreshToken.for_user(user)
                        
            return Response({
              'message':'login was succesfull',
              'refresh':str(refresh) ,
              'access': str(refresh.access_token),
            },status=status.HTTP_200_OK)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


# -------------------------- Change password -------------------------------------------


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        serializer = ChangePasswordSerializer(data =request.data)
        
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            if not user.check_password(old_password):
                return Response({'error':'old password is correct'},status=status.HTTP_200_OK)
            
            user.set_password(new_password)
            user.save()
            
            return Response({'message':'Password Changed succesfully '},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            


# -------------------------- Logout -------------------------------------------
   
class Logout(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'logout was succesfull'},status=status.HTTP_200_OK)
        except Exception:
            return Response({'message':'logout failed'},status=status.HTTP_400_BAD_REQUEST)




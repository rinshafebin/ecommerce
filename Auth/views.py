from rest_framework.views import APIView
from Auth.serializers import UserRegistrationSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from Auth.models import CustomUser

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404 



# Create your views here.
# --------------------------  registration  -------------------------------------------

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
                      
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk)) 
            token = default_token_generator.make_token(user)
            verification_link = f"http://{current_site.domain}{reverse('emailverify', kwargs={'uidb64':uid,'token':token})}"
            
            subject = 'Activate Your Account'
            message = f'hi{user.username},\nPlease click the link below to verify your email and activate your account : \n{verification_link}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject,message,from_email,recipient_list,fail_silently = False)

            
                                                        
            return Response({'message':'user created succesfully ,please check your mail to verify your account'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# ----------------     email verification    -------------------------------------



class EmailVerify(APIView):
    def get(self,request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(CustomUser,pk=uid)
        except(CustomUser.DoesNotExist):
            user = None
            
        if user and default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)




    
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
            



# --------------------------------- reset password -------------------------------------

class ResetPassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        email = request.data.get('email')
        if not email:
            return Response({'error':'email is required'},status=status.HTTP_400_BAD_REQUEST)
        
        try :
            user =CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist :
            return Response({'error':'user not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        current_site = get_current_site(request)
        reset_link = f"http://{current_site.domain}/auth/resetpassword/{uid}/{token}/"
        
        send_mail(
            subject='Reset Your Password',
            message=f"Click the link below to reset your password:\n{reset_link}",
            from_email='admin@myshop.com',
            recipient_list=[user.email],
        )
        return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)




# --------------------------------- setting a new password ----------------------------------

class ResetPasswordview(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,uidb64,token):
        try :
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except CustomUser.DoesNotExist:
            return Response({'error':'user not found '},status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user,token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error':'password is required '},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)




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



# -----------------------------------------  ------------------------------------------------
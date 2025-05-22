from rest_framework.views import APIView
from Auth.serializers import UserRegistrationSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from Auth.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password


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
            
            return Response({'message':'user created succesfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
# -------------------------- Login  -------------------------------------------
   
class Login(APIView):
    def post(self,request):
        serilaizer = LoginSerializer(data=request.data)
        if serilaizer.is_valid():
            user = serilaizer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            is_admin = user.is_staff
            
            return Response({
              'message':'login was succesfull',
              'admin':is_admin,
              'refresh':str(refresh) ,
              'access': str(refresh.access_token),
            },status=status.HTTP_200_OK)
        return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


# -------------------------- Change password -------------------------------------------


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        serializer = ChangePasswordSerializer()
        
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




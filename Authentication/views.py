from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from Authentication.serializers import UserRegistrationSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
Custom_user = get_user_model()

class UserRegistration(APIView):
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user created succesfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
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




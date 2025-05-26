from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from Auth.models import CustomUser

# ------------------------user registration serializer ---------------------------




class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  
    class Meta:
        model = CustomUser
        fields = ['username','email','password','password2']       
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords do not match...')
        return data  
         

# ---------------------------- login serializer ---------------------------



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField() 
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = CustomUser
        fields = ['email','password']
    
    def validate(self,data):
        user =authenticate(email=data['email'],password =data['password'])
        if user and user.is_active:
            return {'user':user}
        raise serializers.ValidationError('invalid email or password')

        
    
                
    # def validate(self,data):
    #     email = data.get('email')
    #     password=data.get('password')       
    #     if email and password:
    #         user =authenticate(username=email,password=password)
    #         if not user :
    #             raise serializers.ValidationError('invalid email or password')
    #     else:
    #         raise serializers.ValidationError('Both email and password are required')    
    #     data['user'] = user
    #     return data
        

 
 
# ------------------------change password serializer ---------------------------
   


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)


    

# ---------------------- Reset password serializer ---------------------------
   


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    
    def validate_email(self,value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('email not found')
        return value
   

class SetNewPassword(serializers.Serializer):
    new_password = serializers.CharField()
    
    

# -----------------------------------------------    -------------------------------   
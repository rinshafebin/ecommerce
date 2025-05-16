from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from Authentication.models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  
    class Meta:
        model = CustomUser
        fields = ['username','email','password','password2']
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords do not match...')
        return data
        
    def create(self,validated_data):
        validated_data.pop('password2')
        validated_data['password']=make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)




class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField() 
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = CustomUser
        fields = ['email','password']
    
    def validate(self,data):
        email = data.get('email')
        password=data.get('password')       
        
        if email and password:
            user =authenticate(username=email,password=password)
            if not user :
                raise serializers.ValidationError('invalid email or password')
        else:
            raise serializers.ValidationError('Both email and password are required')    
        data['user'] = user
        return data
        
    
    
   

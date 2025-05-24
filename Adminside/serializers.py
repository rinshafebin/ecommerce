from rest_framework import serializers
from Auth.models import CustomUser


class ViewAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','is_active','date_joined']



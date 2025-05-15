from rest_framework import serializers
from Admin.models import Category,Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ProductManagementSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
     
    class Meta:       
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at','updated_at']
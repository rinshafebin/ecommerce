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
        
        
    def validate_name(self,value):
        if not value:
           raise serializers.ValidationError('Product name is required')
        if len(value)>3:
            raise serializers.ValidationError('Product must have atleast 3 characters')
        return value
    
    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError('Price must be positive integer')
        return value
    
    def validate_stock(self,value):
        if value<=0:
            raise serializers.ValidationError('Stock cannot be negative')
        return value
    
    
    
    
    
        
        
        
        
        
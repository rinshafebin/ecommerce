from rest_framework import serializers
from products.models import Product
from Auth.models import CustomUser


class ViewAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','is_active','date_joined']


# ----------------------- product serializer ----------------------------------------

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Product.CATEGORY_CHOICES)
    
    class Meta:       
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
           
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError('Product name is required')
        if len(value) < 3:
            raise serializers.ValidationError('Product must have at least 3 characters')
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be positive')
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return value


# ------------------------- product serilizer ends --------------------------------------
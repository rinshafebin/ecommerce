from rest_framework import serializers
from products.models import Product 
from cart.models import OrderItem

class AddToCartItemSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1,default=1) 
    
    def validate_product_id(self,value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("product not found")
        return value


class AddToWishlistSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    
    
    def validate_product_id(self,value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("product not found")
        return value
    
    
    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
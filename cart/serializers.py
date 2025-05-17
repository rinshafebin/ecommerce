from rest_framework import serializers
from cart.models import Cart,CartItem
from AdminUser import Product

class CartItemSerializer(serializers.ModelSerializer):    
    model = CartItem
    fields = ['id','product','quantity']
       
    def validate_quantity(self,value):
        if value < 1:
            raise serializers.ValidationError('quantity must be atleast one')
        return value
    
    def validate_product(self,value):
        if not Product.objects.filter(id=value.id).exists()
        raise serializers.ValidationError('Product does not exists')
        
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only = True)
     
    class Meta:
        model = Cart
        fields = ['user','created_at','items']

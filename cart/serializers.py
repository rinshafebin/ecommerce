from rest_framework import serializers
from cart.models import Cart,CartItem

class CartItemSerializer(serializers.ModelSerializer):    
    model = CartItem
    fields = ['id','product','quantity']
    
    
    def validate_quantity(self,value):
        if value < 1:
            raise serializers.ValidationError('quantity must be atleast one')
        return value
    
    def validate(self,data):
        cart = data.get('cart')
        
        
        


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only = True)
     
    class Meta:
        model = Cart
        fields = ['user','created_at','items']

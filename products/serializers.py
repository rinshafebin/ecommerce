from rest_framework import serializers
from products.models import Products
    
class ProductSerializer(serializers.ModelSerializer):
    model = Products
    fields = '__all__'
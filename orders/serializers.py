from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product



class OrderedItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'product_price', 'quantity']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderedItemSerializer(many=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'created_at', 'is_paid', 'items']
        read_only_fields = ['id', 'user', 'total_price', 'created_at', 'is_paid']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        print("its_user",user)

        order = Order.objects.create(user=user, total_price=0, is_paid=False)
        total_price = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total_price += product.price * quantity

        order.total_price = total_price
        order.save()

        return order

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem,WishList,WishListItem
from cart.serializers import AddToCartItemSerializer,AddToWishlistSerializer
from products.models import Product


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = AddToCartItemSerializer(data = request.data)
        if serializer.is_valid():
            user =request.user
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            product = Product.objects.get(id=product_id)
            cart,_ = Cart.objects.get_or_create(user=user)  
            cart_item,created = CartItem.objects.get_or_create(cart=cart,product=product) 
            
            if not created:
                cart_item.quantity += quantity
            else :
                cart_item.quantity = quantity    
            
            cart_item.save()
            

            return Response({
                'message': 'Product added to cart',
                "product_id": product.id,
                "name" :product.name,
                "quantity": cart_item.quantity
                
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class AddToWishView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = AddToWishlistSerializer(data = request.data)
        if serializer.is_valid():
            user =request.user
            product_id = serializer.validated_data['product_id']
            product = Product.objects.get(id = product_id)
            
            wishlist , _ = WishList.objects.get_or_create(user=user)
            item,created = WishListItem.objects.get_or_create(wishlist=wishlist,product=product)
            
            if not created :
                return Response({"message": "Product already in wishlist "}, status=status.HTTP_200_OK)            
            return Response({"message": "Product added to wishlist."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
 
            
            


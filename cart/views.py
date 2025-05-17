from rest_framework.views import APIView
from cart.models import Cart,CartItem
from cart.serializers import CartItemSerializer,CartSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,user_id):
        cart = Cart.objects.filter(user__id = user_id)
        serializer = CartSerializer(cart,many=True)
        return Response(serializer.data)

class AddProductsToCart(APIView):
        permission_classes = [IsAuthenticated]

    def post(self,request,user_id):

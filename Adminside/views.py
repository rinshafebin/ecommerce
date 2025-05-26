from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from products.serializers import ProductSerializer
from Adminside.serializers import ViewAllUsersSerializer
from rest_framework.response import Response 
from products.models import Product
from Auth.models import CustomUser
from rest_framework import status
from orders.models import Order
from orders.serializers import OrderItemSerializer

# Create your views here.


# --------------------------------------- user apis for viewing ------------------------------------------

class ViewAllUsers(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = ViewAllUsersSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self,request,pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = ViewAllUsersSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
      
    

# ---------------------------------- product apis for CRUD ----------------------------------------------#


class Products(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        products = Product.objects.all()
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No products found'}, status=status.HTTP_204_NO_CONTENT)
    

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            product = Product.objects.create(
                name = validated_data['name'],
                description = validated_data['description'],
                price = validated_data['price'],
                category = validated_data['category'],
                stock = validated_data.get('stock',0),
                image = validated_data.get('image',None),
                
            )
            response_serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        
# ----------------------------- crud product --------------------------------

class ProductDetails(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)

   
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'detail': 'Eror updating product'}, status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'detail': 'product deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)
        
        except:    
            return Response({'detail': 'error deleting the product'},status=status.HTTP_404_NOT_FOUND)
        
        
    
# ---------------------------- products viewing by category  --------------------------


class ViewProductsByCategory(APIView):
    permission_classes = [IsAdminUser]     
    
    def get(self, request, category):
        try:
            products = Product.objects.filter(category=category)
            if products.exists():
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)          
            return Response({'detail': 'no product found for this category'}, status=status.HTTP_204_NO_CONTENT)
        
        except:
            return Response({'detail': 'error fetching products by category'}, status=status.HTTP_400_BAD_REQUEST)
               





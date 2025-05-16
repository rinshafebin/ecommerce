from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from Admin.serializers import ProductSerializer,ViewAllUsersSerializer
from rest_framework.response import Response 
from Admin.models import Product
from Authentication.models import CustomUser
from rest_framework import status
# Create your views here.


# --------------------------------------- user apis for viewing ------------------------------------------

class ViewAllUsers(APIView):
    
    def get(self,request):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = ViewAllUsersSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

        
class ViewSpecificUser(APIView):
    def get(self,request,pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = ViewAllUsersSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    


# ---------------------------------- product apis for CRUD ----------------------------------------------#

class ProductCreate(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Productlist(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        products = Product.objects.all()
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No products found'}, status=status.HTTP_204_NO_CONTENT)
 
 
        
class ViewProduct(APIView):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
       
        
     
class ProductUpdate(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    
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
               


class ProductDelete(APIView):
    permission_classes = [IsAdminUser]
   
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'detail': 'product deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)
        
        except:    
            return Response({'detail': 'error deleting the product'},status=status.HTTP_404_NOT_FOUND)


# ----------------------------------------------- product apis end ------------------------------------------
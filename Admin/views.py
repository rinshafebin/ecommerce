from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from Admin.serializers import ProductManagementSerializer
from Admin.models import Product
from rest_framework.response import Response 
from rest_framework import status
# Create your views here.





class ProductlistApi(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        products = Product.objects.all()
        if products.exists():
            serializer = ProductManagementSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No products found'}, status=status.HTTP_204_NO_CONTENT)
        

class ProductCreateApi(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = ProductManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ProductUpdateApi(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    
    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductManagementSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'detail': 'Eror updating product'}, status=status.HTTP_404_NOT_FOUND)


class ViewProductsByCategory(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, category_id):
        try:
            products = Product.objects.filter(category_id=category_id)
            if products.exists():
                serializer = ProductManagementSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)          
            return Response({'detail': 'no product found for this category'}, status=status.HTTP_204_NO_CONTENT)
        
        except:
            return Response({'detail': 'error fetching products by category'}, status=status.HTTP_400_BAD_REQUEST)
               

class ProductDeleteApi(APIView):
    permission_classes = [IsAdminUser]
    
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({'detail': 'product deleted succesfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'detail': 'error deleting the product'})

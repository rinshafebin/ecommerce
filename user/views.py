from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from products.serializers import ProductSerializer
from rest_framework.response import Response 
from products.models import Product
from rest_framework import status
# Create your views here.


# ---------------------- all products  ---------------------------

class Products(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        products = Product.objects.all()
        if products.exists():
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No products found'}, status=status.HTTP_204_NO_CONTENT)


class ProductDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)



# ---------------------- products viewing by category  --------------

class ViewProductsByCategory(APIView):
    permission_classes = [IsAuthenticated]
     
    def get(self, request, category):
        try:
            products = Product.objects.filter(category=category)
            if products.exists():
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)          
            return Response({'detail': 'no product found for this category'}, status=status.HTTP_204_NO_CONTENT)
        
        except:
            return Response({'detail': 'error fetching products by category'}, status=status.HTTP_400_BAD_REQUEST)
               


# ------------------------------------------------------------------------
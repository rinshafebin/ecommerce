from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser,FormParser
from Admin.serializers import ProductManagementSerializer
from Admin.models import Product,Category
from rest_framework.response import Response 
from rest_framework import status
from django.http import Http404
# Create your views here.

class AdminProductApi(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser,FormParser]
    
    def get_product(self,pk):
        try :
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404('product not found')
        
    def get(self,request,pk=None):
        try:
            if pk:
                product = self.get_product(pk)
                serializer =ProductManagementSerializer(product)
                return Response(serializer.data)
            else:
                products = product.objects.all()
                serializer = ProductManagementSerializer(products,many=True)
                return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
            
    # def post(self,request):
    #     try:
    #         serializer = ProductManagementSerializer()
        
        
            
        
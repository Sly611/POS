from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import * 
from .models import Category, Product, Order, Payment
from .serializers import *


#=============================================================================================================
# Create your views here.
#=============================================================================================================
def get_list(entity,serializer):
    data = entity.objects.all()
    json = serializer(data, many=True)
    return json


# #=============================================================================================================
# THIS VIEW RETURNS A LIST OF PRODUCT OBJECTS
# #=============================================================================================================    
class ProductListView(APIView):
    def get(self, request):
        serializer = get_list(Product, ProductSerializer)
        return Response(serializer.data)        
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#=============================================================================================================
# THIS VIEW REQUESTS A SINGLE PRODUCT OBJECT
#=============================================================================================================
class ProductDetailView(APIView):

    def get(self, request, pk, format=None):
        data = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(data)
        return Response(serializer.data)
        
    def put(self, request, pk):
        data = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk):
        data = get_object_or_404(Product, pk=pk)
        data.delete() 
        return Response(status=HTTP_200_OK)

        

#=============================================================================================================
# THIS VIEW RETURNS A LIST OF CATEGORY OBJECTS
#=============================================================================================================
class CategoryListView(APIView):
    def get(self, request):
        serializer = get_list(Category, CategorySerializer)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#=============================================================================================================
# THIS VIEW REQUESTS A SINGLE CATEGORY OBJECT
#=============================================================================================================
class CategoryDetailView(APIView):

    def get(self, request, pk, format=None):
        data = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(data)
        return Response(serializer.data)
        
    def put(self, request, pk):
        data = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk):
        data = get_object_or_404(Category, pk=pk)
        data.delete() 
        return Response(status=HTTP_204_NO_CONTENT)



#=============================================================================================================
# THIS VIEW RETURNS A LIST OF ORDER OBJECTS
#=============================================================================================================
class OrderListView(APIView):
    def get(self, request):
        serializer = get_list(Order, OrderSerializer)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
#=============================================================================================================
# THIS VIEW REQUESTS A SINGLE ORDER OBJECT
#=============================================================================================================
class OrderDetailView(APIView):

    def get(self, request, pk, format=None):
        data = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(data)
        return Response(serializer.data)

        
    def put(self, request, pk):
        data = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 


    def delete(self, request, pk):
        data = get_object_or_404(Order, pk=pk)
        data.delete() 
        return Response(status=HTTP_200_OK)




#=============================================================================================================
# THIS VIEW RETURNS A LIST OF PAYMENT OBJECTS
#=============================================================================================================
class PaymentView(APIView):
    def get(self, request):
        serializer = get_list(Payment, PaymentSerializer)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

#=============================================================================================================
# THIS VIEW FILTERS THE PRODUCTS BASED ON THE SPECIFIED ATTRIBUTE
#=============================================================================================================
class ProductSearchAPIView(APIView):

    def get(self, request):
        name = request.query_params.get('name',None)
        category = request.query_params.get('category', None)
        upcode = request.query_params.get('upc', None)
        price = request.query_params.get('price', None)
        size = request.query_params.get('size', None)

        queryset = Product.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        elif category:
            queryset = queryset.filter(category__name__icontains=category)
        elif upcode:
            queryset = queryset.filter(upc__exact=upcode)
        elif price:
            queryset.filter(selling_price__exact=price)
        elif size:
            queryset = queryset.filter(size__iexact=size)
        else:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    

#=============================================================================================================
# THIS VIEW FILTER ORDERS ACCORDING TO THE SPECIFIED ATTRIBUTE
#=============================================================================================================
class OrderSearchAPIView(APIView):

    def get(self, request):

        status = request.query_params.get('status', None)
        payment_method = request.query_params.get('payment',None)
        date_created = request.query_params.get('date_created, None')
        from_date = request.query_params.get('from_date', None)
        upto_date = request.query_params.get('upto_date', None)

        queryset = Order.objects.all()

        if status:
            queryset = queryset.filter(status__name__icontains=status)
        elif payment_method:
            queryset = queryset.filter(payment_method__name__icontains=payment_method)
        elif from_date:
            queryset = queryset.filter(date_created__gte=from_date)
        elif upto_date:
            queryset = queryset.filter(date_created__lte=upto_date)
        elif from_date:
            queryset = queryset.filter(date_created__exact=date_created)            
        else:
            return Response(status=HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

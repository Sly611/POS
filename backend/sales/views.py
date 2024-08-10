from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import * 
from .models import Category, Product, Order, Payment, CancelledOrdersTracker
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
    
# #=============================================================================================================
# THIS VIEW CREATES A PRODUCT OBJECT
# #=============================================================================================================    
class ProductCreateView(APIView):
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
    
#=============================================================================================================
# THIS VIEW CREATES A CATEGORY OBJECT
#=============================================================================================================
class CategoryCreateView(APIView):    
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
        return Response(status=HTTP_200_OK)



#=============================================================================================================
# THIS VIEW RETURNS A LIST OF ORDER OBJECTS
#=============================================================================================================
class OrderListView(APIView):
    def get(self, request):
        serializer = get_list(Order, OrderSerializer)
        return Response(serializer.data)
    

#=============================================================================================================
# THIS VIEW CREATES A ORDER OBJECT
#=============================================================================================================
class OrderCreateView(APIView):

    def calculate_total_price(self, order):
        total_price = 0
        for item in order.get_order_items():
            total_price += item.amount
        order.total_amount = total_price


    def post(self, request):
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            self.calculate_total_price(order)
            order.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

# #=============================================================================================================
# # THIS VIEW CREATES A ORDER OBJECT
# #=============================================================================================================
# class OrderCheckoutView(APIView):

#     def update_status(self, pk):
#         order = Order.objects.get(id=pk)
#         order.status = "completed"

#     def put(self, request, pk):

#         data = get_object_or_404(Order, pk)
#         serializer = OrderSerializer(data, data=request.data)
#         if serializer.is_valid():
#             self.update_status(pk)
#             serializer.save()
#             return Response(serializer.data, status=HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#=============================================================================================================
# THIS VIEW DELETES THE SPECIFIED ORDER
#=============================================================================================================
class OrderCancelView(APIView):

    def delete(self, request, pk):
        data = get_object_or_404(Order, pk=pk)
        CancelledOrdersTracker.objects.create()
        data.delete() 
        return Response({"detail": "Order successfully canceled."}, status=HTTP_204_NO_CONTENT)
    

#=============================================================================================================
# THIS VIEW REQUESTS A SINGLE ORDER OBJECT
#=============================================================================================================
class OrderDetailView(APIView):

    def get(self, request, pk, format=None):
        data = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(data)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     data = get_object_or_404(Order, pk=pk)
    #     serializer = OrderSerializer(data, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=HTTP_202_ACCEPTED)
    #     else:
    #         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 

    # def delete(self, request, pk):
    #     data = get_object_or_404(Order, pk=pk)
    #     data.delete() 
    #     return Response(status=HTTP_200_OK)



#=============================================================================================================
# THIS VIEW CREATES A ORDER OBJECT
#=============================================================================================================
class CheckStockView(APIView):

    def check_stock(self, product, data):
        return product.quantity > data['quantity']

    def post(self, request):
        data = request.data
        product = Product.objects.get(id=data['id'])
        if self.check_stock(product, data):
            return Response(status=HTTP_200_OK)
        else:
            return Response({"message": "Requested quantity exceeds available stock"})

        
        

#=============================================================================================================
# THIS VIEW REQUESTS A SINGLE ORDER_ITEM OBJECT
#=============================================================================================================
class OrderItemDetailView(APIView):

    def get(self, request, pk):
        data = get_object_or_404(Order_item, pk)
        serializer = Order_itemSerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)  

    def put(self, request, pk):
        data = get_object_or_404(Order_item, pk)
        serializer = Order_itemSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)                    
            


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
            queryset = queryset.filter(status__icontains=status)
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

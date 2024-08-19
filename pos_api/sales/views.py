from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import * 
from .models import Category, Product, Order, Payment, CancelledOrdersTracker
from .serializers import *
from .schema import *


#===================================================================================================================================================
# Create your views here.
#===================================================================================================================================================
def get_list(entity,serializer):
    data = entity.objects.all()
    json = serializer(data, many=True)
    return json


# #===================================================================================================================================================
# THIS VIEW RETURNS A LIST OF PRODUCT OBJECTS
# #===================================================================================================================================================   
class ProductListView(APIView):

    @product_list_schema
    def get(self, request):
        """
        Handle GET requests to retrieve a list of products.

        This method serializes a list of `Product` instances using 
        `ProductSerializer` and returns the serialized data in the response.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A Response object containing serialized data 
            of the `Product` instances.
        """
        serializer = get_list(Product, ProductSerializer)
        return Response(serializer.data)        
    
# #===================================================================================================================================================
# THIS VIEW CREATES A PRODUCT OBJECT
# #===================================================================================================================================================    
class ProductCreateView(APIView):
    
    @product_create_schema
    def post(self, request):
        """
        Handle POST requests to create a new product.

        This method deserializes the incoming data using `ProductSerializer`,
        validates it, and if valid, saves the new `Product` instance to the database.
        It returns the serialized data of the created product or validation errors.

        Args:
            request (HttpRequest): The HTTP request object containing product data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                created `Product` instance and a status of `HTTP_201_CREATED` 
                if the data is valid.
                - A Response object containing validation errors and a status 
                of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#===================================================================================================================================================
# THIS VIEW REQUESTS A SINGLE PRODUCT OBJECT
#===================================================================================================================================================
class ProductDetailView(APIView):

    """
    View to handle retrieval, update, and deletion of a single product.

    This view supports GET, PUT, and DELETE HTTP methods for interacting 
    with individual `Product` instances identified by their primary key (pk).

    Methods:
        get(request, pk, format=None):
            Retrieve and return a product based on its primary key.

        put(request, pk):
            Update a product based on its primary key with the provided data.

        delete(request, pk):
            Delete a product based on its primary key.
    """
    @product_detail_schema
    def get(self, request, pk, format=None):
        """
        Retrieve a single product by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Product` to retrieve.
            format (str, optional): The format of the response (default is None).

        Returns:
            Response: A Response object containing serialized data of the 
            `Product` instance.
        """
        data = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(data)
        return Response(serializer.data)
    
    @product_detail_schema    
    def put(self, request, pk):
        """
        Update a single product by its primary key.

        Args:
            request (HttpRequest): The HTTP request object containing product data.
            pk (int): The primary key of the `Product` to update.

        Returns:
            Response: 
                - A Response object containing serialized data of the updated 
                  `Product` instance and a status of `HTTP_202_ACCEPTED` 
                  if the data is valid.
                - A Response object containing validation errors and a status 
                  of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """

        data = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 

    @product_detail_schema
    def delete(self, request, pk):
        """
        Delete a single product by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Product` to delete.

        Returns:
            Response: A Response object with a status of `HTTP_200_OK`.
        """
        data = get_object_or_404(Product, pk=pk)
        data.delete() 
        return Response(status=HTTP_200_OK)


#===================================================================================================================================================
# THIS VIEW RETURNS A LIST OF CATEGORY OBJECTS
#===================================================================================================================================================
class CategoryListView(APIView):
    """
    View to handle retrieving a list of categories.

    This view supports the GET HTTP method to retrieve and return a list 
    of all `Category` instances.

    Methods:
        get(request):
            Retrieve and return a list of all categories.
    """
    @category_list_schema
    def get(self, request):
        """
        Retrieve a list of all categories.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A Response object containing serialized data of the 
            `Category` instances.
        """
        serializer = get_list(Category, CategorySerializer)
        return Response(serializer.data)


#===================================================================================================================================================
# THIS VIEW CREATES A CATEGORY OBJECT
#===================================================================================================================================================
class CategoryCreateView(APIView):
    """
    View to handle creating a new category.

    This view supports the POST HTTP method to create a new `Category` instance.

    Methods:
        post(request):
            Create a new category with the provided data.
    """
    @category_create_schema
    def post(self, request):
        """
        Create a new category.

        This method deserializes the incoming data using `CategorySerializer`,
        validates it, and if valid, saves the new `Category` instance to the database.
        It returns the serialized data of the created category or validation errors.

        Args:
            request (HttpRequest): The HTTP request object containing category data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Category` instance and a status of `HTTP_201_CREATED` 
                  if the data is valid.
                - A Response object containing validation errors and a status 
                  of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """ 
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

#===================================================================================================================================================
# THIS VIEW REQUESTS A SINGLE CATEGORY OBJECT
#===================================================================================================================================================
class CategoryDetailView(APIView):
    """
    View to handle retrieval, update, and deletion of a single category.

    This view supports GET, PUT, and DELETE HTTP methods for interacting 
    with individual `Category` instances identified by their primary key (pk).

    Methods:
        get(request, pk, format=None):
            Retrieve and return a category based on its primary key.

        put(request, pk):
            Update a category based on its primary key with the provided data.

        delete(request, pk):
            Delete a category based on its primary key.
    """
    @category_detail_schema
    def get(self, request, pk, format=None):
        """
        Retrieve a single category by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Category` to retrieve.
            format (str, optional): The format of the response (default is None).

        Returns:
            Response: A Response object containing serialized data of the 
            `Category` instance.
        """
        data = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(data)
        return Response(serializer.data)
    
    @category_detail_schema
    def put(self, request, pk):
        """
        Update a single category by its primary key.

        Args:
            request (HttpRequest): The HTTP request object containing category data.
            pk (int): The primary key of the `Category` to update.

        Returns:
            Response: 
                - A Response object containing serialized data of the updated 
                  `Category` instance and a status of `HTTP_202_ACCEPTED` 
                  if the data is valid.
                - A Response object containing validation errors and a status 
                  of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        data = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST) 

    @category_detail_schema
    def delete(self, request, pk):
        """
        Delete a single category by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Category` to delete.

        Returns:
            Response: A Response object with a status of `HTTP_200_OK`.
        """
        data = get_object_or_404(Category, pk=pk)
        data.delete()
        return Response(status=HTTP_200_OK)


#===================================================================================================================================================
# THIS VIEW RETURNS A LIST OF ORDER OBJECTS
#===================================================================================================================================================
class OrderListView(APIView):
    """
    View to handle retrieving a list of orders.

    This view supports the GET HTTP method to retrieve and return a list 
    of all `Order` instances.

    Methods:
        get(request):
            Retrieve and return a list of all orders.
    """
    @order_list_schema
    def get(self, request):
        """
        Retrieve a list of all orders.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A Response object containing serialized data of the 
            `Order` instances.
        """
        serializer = get_list(Order, OrderSerializer)
        return Response(serializer.data)


#===================================================================================================================================================
# THIS VIEW CREATES A ORDER OBJECT
#===================================================================================================================================================
class OrderCreateView(APIView):
    """
    View to handle creating a new order and calculating its total price.

    This view supports the POST HTTP method to create a new `Order` instance,
    and it includes a helper method to calculate the total price of the order 
    based on its items.

    Methods:
        calculate_total_price(order):
            Calculate and set the total price for a given order.

        post(request):
            Create a new order with the provided data and calculate its total price.
    """
    def calculate_total_price(self, order):
        """
        Calculate the total price for an order.

        This method sums the amount of each item in the order and sets 
        the `total_amount` field of the `Order` instance.

        Args:
            order (Order): The `Order` instance for which the total price 
            is to be calculated.
        """
        total_price = 0
        for item in order.get_order_items():
            total_price += item.amount
        order.total_amount = total_price

    @order_create_schema
    def post(self, request):
        """
        Create a new order and calculate its total price.

        This method deserializes the incoming data using `OrderSerializer`,
        validates it, and if valid, saves the new `Order` instance to the database.
        It then calculates the total price of the order, saves the updated order, 
        and returns the serialized data of the created order or validation errors.

        Args:
            request (HttpRequest): The HTTP request object containing order data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Order` instance and a status of `HTTP_201_CREATED` 
                  if the data is valid.
                - A Response object containing validation errors and a status 
                  of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        data = request.data
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            self.calculate_total_price(order)
            order.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        

#===================================================================================================================================================
# THIS VIEW DELETES THE SPECIFIED ORDER
#===================================================================================================================================================
class OrderCancelView(APIView):
    """
    View to handle canceling an order.

    This view supports the DELETE HTTP method to delete an `Order` instance
    and track the cancellation.

    Methods:
        delete(request, pk):
            Cancel an order by its primary key and track the cancellation.
    """

    @order_cancel_schema
    def delete(self, request, pk):
        """
        Cancel an order and track the cancellation.

        This method retrieves an `Order` instance by its primary key, 
        tracks the cancellation by creating an entry in `CancelledOrdersTracker`, 
        deletes the order, and returns a success message.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Order` to cancel.

        Returns:
            Response: A Response object with a success message and a status of 
            `HTTP_204_NO_CONTENT`.
        """
        data = get_object_or_404(Order, pk=pk)
        CancelledOrdersTracker.objects.create()
        data.delete()
        return Response({"detail": "Order successfully canceled."}, status=HTTP_204_NO_CONTENT)

    
#===================================================================================================================================================
# THIS VIEW REQUESTS A SINGLE ORDER OBJECT
#===================================================================================================================================================
class OrderDetailView(APIView):
    """
    View to handle retrieving the details of a single order.

    This view supports the GET HTTP method to retrieve and return the 
    details of an individual `Order` instance identified by its primary key (pk).

    Methods:
        get(request, pk, format=None):
            Retrieve and return the details of an order based on its primary key.
    """
    @order_detail_schema
    def get(self, request, pk, format=None):
        """
        Retrieve the details of a single order by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Order` to retrieve.
            format (str, optional): The format of the response (default is None).

        Returns:
            Response: A Response object containing serialized data of the 
            `Order` instance.
        """
        data = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(data)
        return Response(serializer.data)


#===================================================================================================================================================
# THIS VIEW CREATES A ORDER OBJECT
#===================================================================================================================================================
class CheckStockView(APIView):
    """
    View to handle checking stock availability for a product.

    This view supports the POST HTTP method to check if the requested quantity
    of a product is available in stock.

    Methods:
        check_stock(product, data):
            Check if the requested quantity for a product is available in stock.

        post(request):
            Check the stock availability for a product based on the provided data.
    """
    def check_stock(self, product, data):
        """
        Check if the requested quantity of a product is available in stock.

        Args:
            product (Product): The `Product` instance to check.
            data (dict): A dictionary containing the requested quantity under the key 'quantity'.

        Returns:
            bool: True if the available quantity is greater than the requested quantity, False otherwise.
        """
        return product.quantity > data['quantity']

    @check_stock_schema
    def post(self, request):
        """
        Check the stock availability for a product.

        This method retrieves the `Product` instance based on the provided product ID,
        checks if the requested quantity is available, and returns an appropriate response.

        Args:
            request (HttpRequest): The HTTP request object containing product ID and quantity.

        Returns:
            Response: 
                - A Response object with a status of `HTTP_200_OK` if the requested quantity is available.
                - A Response object with a message indicating that the requested quantity exceeds 
                  available stock if the quantity is not available.
        """
        data = request.data
        product = Product.objects.get(id=data['id'])
        if self.check_stock(product, data):
            return Response(status=HTTP_200_OK)
        else:
            return Response({"message": "Requested quantity exceeds available stock"})


#===================================================================================================================================================
# THIS VIEW REQUESTS A SINGLE ORDER_ITEM OBJECT
#===================================================================================================================================================
class OrderItemDetailView(APIView):

    def get(self, request, pk):
        data = get_object_or_404(Order_item, pk)
        serializer = Order_itemSerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)  


#===================================================================================================================================================
# THIS VIEW RETURNS A LIST OF PAYMENT OBJECTS
#===================================================================================================================================================
class PaymentView(APIView):
    """
    View to handle retrieving and creating payments.

    This view supports GET and POST HTTP methods to interact with `Payment` instances.

    Methods:
        get(request):
            Retrieve and return a list of all payments.

        post(request):
            Create a new payment with the provided data.
    """
    @payment_schema
    def get(self, request):
        """
        Retrieve a list of all payments.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A Response object containing serialized data of all 
            `Payment` instances.
        """
        serializer = get_list(Payment, PaymentSerializer)
        return Response(serializer.data)
    
    @payment_schema
    def post(self, request):
        """
        Create a new payment.

        This method deserializes the incoming data using `PaymentSerializer`,
        validates it, and if valid, saves the new `Payment` instance to the database.
        It returns the serialized data of the created payment or validation errors.

        Args:
            request (HttpRequest): The HTTP request object containing payment data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Payment` instance and a status of `HTTP_201_CREATED` 
                  if the data is valid.
                - A Response object containing validation errors and a status 
                  of `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#===================================================================================================================================================
# THIS VIEW FILTERS THE PRODUCTS BASED ON THE SPECIFIED ATTRIBUTE
#===================================================================================================================================================
class ProductSearchAPIView(APIView):
    """
    View to handle searching for products based on query parameters.

    This view supports the GET HTTP method to search for `Product` instances 
    based on various query parameters such as name, category, UPC, price, 
    and size.

    Methods:
        get(request):
            Search for products based on query parameters and return the results.
    """

    @product_search_schema
    def get(self, request):
        """
        Search for products based on the provided query parameters.

        This method retrieves query parameters from the request to filter 
        `Product` instances. It applies the filters for name, category, UPC, 
        price, and size as specified in the query parameters and returns the 
        filtered list of products.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.

        Returns:
            Response: 
                - A Response object containing serialized data of the filtered 
                  `Product` instances if matches are found.
                - A Response object with a status of `HTTP_404_NOT_FOUND` if no 
                  products match the query parameters.
        """
        name = request.query_params.get('name', None)
        category = request.query_params.get('category', None)
        upcode = request.query_params.get('upc', None)
        price = request.query_params.get('price', None)
        size = request.query_params.get('size', None)

        queryset = Product.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if upcode:
            queryset = queryset.filter(upc__exact=upcode)
        if price:
            queryset = queryset.filter(selling_price__exact=price)
        if size:
            queryset = queryset.filter(size__iexact=size)
        
        if not queryset.exists():
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(queryset, many=True)
        
        return Response(serializer.data)


#===================================================================================================================================================
# THIS VIEW FILTER ORDERS ACCORDING TO THE SPECIFIED ATTRIBUTE
#===================================================================================================================================================
class OrderSearchAPIView(APIView):
    """
    View to handle searching for orders based on query parameters.

    This view supports the GET HTTP method to search for `Order` instances 
    based on various query parameters such as status, payment method, 
    date created, from date, and upto date.

    Methods:
        get(request):
            Search for orders based on query parameters and return the results.
    """

    @order_search_schema
    def get(self, request):
        """
        Search for orders based on the provided query parameters.

        This method retrieves query parameters from the request to filter 
        `Order` instances. It applies filters for status, payment method, 
        date created, from date, and upto date as specified in the query 
        parameters and returns the filtered list of orders.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.

        Returns:
            Response: 
                - A Response object containing serialized data of the filtered 
                  `Order` instances if matches are found.
                - A Response object with a status of `HTTP_404_NOT_FOUND` if no 
                  orders match the query parameters.
        """
        status = request.query_params.get('status', None)
        payment_method = request.query_params.get('payment', None)
        date_created = request.query_params.get('date_created', None)
        from_date = request.query_params.get('from_date', None)
        upto_date = request.query_params.get('upto_date', None)

        queryset = Order.objects.all()

        if status:
            queryset = queryset.filter(status__icontains=status)
        if payment_method:
            queryset = queryset.filter(payment_method__name__icontains=payment_method)
        if from_date:
            queryset = queryset.filter(date_created__gte=from_date)
        if upto_date:
            queryset = queryset.filter(date_created__lte=upto_date)
        if date_created:
            queryset = queryset.filter(date_created__exact=date_created)
        
        if not queryset.exists():
            return Response(status=HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

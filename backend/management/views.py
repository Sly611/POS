from rest_framework.status import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expenses
from .serializers import *
from sales.models import Order_item, Order, Product
from django.db.models import Sum
from datetime import datetime, timedelta, date
from django.utils.dateparse import parse_date
import csv
from django.http import HttpResponse


# Create your views here.


def format_date(date):
    return date.strftime('%Y-%m-%d')

# now = datetime.now()
today = datetime.today()
week = today - timedelta(days= today.weekday())
month = datetime.now().month
year = datetime.now().year




TODAY = format_date(today)

CURRENT_WEEK = format_date(week)

CURRENT_MONTH = date(year=year, month=month, day=1)

CURRENT_YEAR = date(year=year, month=1, day=1)




class ExpensesListView(APIView):
    """
    View to handle retrieving a list of expenses.

    This view supports the GET HTTP method to retrieve and return a list 
    of all `Expenses` instances.

    Methods:
        get(request):
            Retrieve and return a list of all expenses.
    """

    def get(self, request):
        """
        Retrieve a list of all expenses.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: 
                - A Response object containing serialized data of all 
                  `Expenses` instances and a status of `HTTP_200_OK`.
        """
        data = Expenses.objects.all()
        serializer = ExpenseSerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ExpensesCreateView(APIView):
    """
    View to handle creating a new expense.

    This view supports the POST HTTP method to create a new `Expense` instance.

    Methods:
        post(request):
            Create a new expense with the provided data.
    """

    def post(self, request):
        """
        Create a new expense.

        This method deserializes the incoming data using `ExpenseSerializer`,
        validates it, and if valid, saves the new `Expense` instance to the database.
        It returns the serialized data of the created expense or an error message 
        if the data is invalid.

        Args:
            request (HttpRequest): The HTTP request object containing expense data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Expense` instance and a status of `HTTP_201_CREATED` 
                  if the data is valid.
                - A Response object containing an error message and a status of 
                  `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({"message": "invalid input"}, status=HTTP_400_BAD_REQUEST)


class ExpensesDetailView(APIView):
    """
    View to handle retrieving, updating, and deleting a single expense.

    This view supports the GET, PUT, and DELETE HTTP methods to interact with 
    an individual `Expenses` instance identified by its primary key (pk).

    Methods:
        get(request, pk):
            Retrieve and return the details of a single expense based on its primary key.

        put(request, pk):
            Update the details of a single expense based on its primary key with the provided data.

        delete(request, pk):
            Delete a single expense based on its primary key.
    """

    def get(self, request, pk):
        """
        Retrieve the details of a single expense by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Expenses` instance to retrieve.

        Returns:
            Response: 
                - A Response object containing serialized data of the `Expenses` instance
                  and a status of `HTTP_200_OK`.
        """
        data = get_object_or_404(Expenses, pk=pk)
        serializer = ExpenseSerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a single expense by its primary key.

        This method deserializes the incoming data using `ExpenseSerializer`,
        validates it, and if valid, updates the `Expenses` instance with the new data.

        Args:
            request (HttpRequest): The HTTP request object containing updated expense data.
            pk (int): The primary key of the `Expenses` instance to update.

        Returns:
            Response: 
                - A Response object containing serialized data of the updated `Expenses` instance
                  and a status of `HTTP_202_ACCEPTED` if the data is valid.
                - A Response object containing an error message and a status of `HTTP_400_BAD_REQUEST`
                  if the data is invalid.
        """
        data = get_object_or_404(Expenses, pk=pk)
        serializer = ExpenseSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response({"message": "invalid input"}, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        """
        Delete a single expense by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Expenses` instance to delete.

        Returns:
            Response: 
                - A Response object with a success message and a status of `HTTP_200_OK` 
                  indicating that the expense was deleted successfully.
        """
        data = get_object_or_404(Expenses, pk=pk)
        data.delete()
        return Response({"message": "deleted successfully"}, status=HTTP_200_OK)

    

class StoreCreateApiView(APIView):
    """
    View to handle listing and creating stores.

    This view supports the GET and POST HTTP methods to interact with `Store` instances.
    - GET method to retrieve and list all stores.
    - POST method to create a new store.

    Methods:
        get(request):
            Retrieve and return a list of all stores.

        post(request):
            Create a new store with the provided data.
    """

    def get(self, request):
        """
        Retrieve a list of all stores.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: 
                - A Response object containing serialized data of all `Store` instances
                  and a status of `HTTP_200_OK`.
        """
        data = Store.objects.all()
        serializer = StoreSerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        """
        Create a new store.

        This method deserializes the incoming data using `StoreSrializer`,
        validates it, and if valid, saves the new `Store` instance to the database.
        It returns the serialized data of the created store or an error message if 
        the data is invalid.

        Args:
            request (HttpRequest): The HTTP request object containing store data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Store` instance and a status of `HTTP_201_CREATED` 
                  if the data is valid.
                - A Response object containing an error message and a status of 
                  `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({"message": "invalid input"}, status=HTTP_400_BAD_REQUEST)

        

class ExpenseCategoryListView(APIView):
    """
    View to handle listing and creating expense categories.

    This view supports the GET and POST HTTP methods to interact with `Expense_category` instances.
    - GET method to retrieve and list all expense categories.
    - POST method to create a new expense category.

    Methods:
        get(request):
            Retrieve and return a list of all expense categories.

        post(request):
            Create a new expense category with the provided data.
    """

    def get(self, request):
        """
        Retrieve a list of all expense categories.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: 
                - A Response object containing serialized data of all `Expense_category` instances
                  and a status of `HTTP_200_OK`.
        """
        data = Expense_category.objects.all()
        serializer = Expense_categorySerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        """
        Create a new expense category.

        This method deserializes the incoming data using `Expense_categorySerializer`,
        validates it, and if valid, saves the new `Expense_category` instance to the database.
        It returns the serialized data of the created expense category.

        Args:
            request (HttpRequest): The HTTP request object containing expense category data.

        Returns:
            Response: 
                - A Response object containing serialized data of the newly 
                  created `Expense_category` instance and a status of `HTTP_201_CREATED`
                  if the data is valid.
        """
        serializer = Expense_categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        

class ExpenseCategoryDetailView(APIView):
    """
    View to handle retrieving, updating, and deleting a single expense category.

    This view provides endpoints to retrieve, update, or delete a specific 
    `Expense_category` instance identified by its primary key (pk).

    Methods:
        get(request, pk):
            Retrieve a single expense category by its primary key.

        put(request, pk):
            Update a single expense category by its primary key with the provided data.

        delete(request, pk):
            Delete a single expense category by its primary key.
    """

    def get(self, request, pk):
        """
        Retrieve a single expense category by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Expense_category` instance to retrieve.

        Returns:
            Response: 
                - A Response object containing serialized data of the `Expense_category` instance
                  and a status of `HTTP_200_OK`.
        """
        data = get_object_or_404(Expense_category, pk=pk)
        serializer = Expense_categorySerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a single expense category by its primary key.

        This method deserializes the incoming data using `Expense_categorySerializer`,
        validates it, and if valid, updates the `Expense_category` instance with the 
        new data. Returns the serialized data of the updated instance.

        Args:
            request (HttpRequest): The HTTP request object containing the updated expense 
                                   category data.
            pk (int): The primary key of the `Expense_category` instance to update.

        Returns:
            Response: 
                - A Response object containing serialized data of the updated `Expense_category` 
                  instance and a status of `HTTP_202_ACCEPTED` if the data is valid.
                - A Response object containing an error message and a status of 
                  `HTTP_400_BAD_REQUEST` if the data is invalid.
        """
        data = get_object_or_404(Expense_category, pk=pk)
        serializer = Expense_categorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        return Response({"message": "invalid input"}, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        """
        Delete a single expense category by its primary key.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the `Expense_category` instance to delete.

        Returns:
            Response: 
                - A Response object containing a success message and a status of `HTTP_200_OK` 
                  indicating that the expense category was deleted successfully.
        """
        data = get_object_or_404(Expense_category, pk=pk)
        data.delete()
        return Response({"message": "deleted successfully"}, status=HTTP_200_OK)



class BestSellingProductView(APIView):
    """
    View to retrieve the top-selling products based on a specified time filter.

    This view supports the GET HTTP method to retrieve the top 5 best-selling 
    products. The products can be filtered by day, week, month, or year based 
    on the `filter` query parameter.

    Methods:
        get(request, format=None):
            Retrieve and return the top 5 best-selling products based on the specified time filter.
    """

    def get(self, request, format=None):
        """
        Retrieve the top 5 best-selling products.

        This method filters `Order_item` instances based on the provided time filter
        (`day`, `week`, `month`, or `year`). It calculates the total quantity sold for
        each product and returns the top 5 products with the highest total quantities.
        
        The available filters are:
            - `day`: Filters sales data for today.
            - `week`: Filters sales data for the current week.
            - `month`: Filters sales data for the current month.
            - `year`: Filters sales data for the current year.
        
        If no filter is provided, all available sales data is used.

        Args:
            request (HttpRequest): The HTTP request object containing the filter parameter.
            format (str, optional): The format of the response (default is None).

        Returns:
            Response: 
                - A Response object containing serialized data of the top 5 best-selling products 
                  and a status of `HTTP_200_OK` if sales data is available.
                - A Response object containing a message indicating no sales data is available 
                  and a status of `HTTP_404_NOT_FOUND` if no sales data matches the filter.
        """
        filter_by = request.query_params.get("filter", None)

        queryset = Order_item.objects.all()
        order_items = None

        if filter_by == "day":
            order_items = queryset.filter(order__date_created__exact=TODAY)

        elif filter_by == "week":
            order_items = queryset.filter(order__date_created__gte=CURRENT_WEEK)
        
        elif filter_by == "month":
            order_items = queryset.filter(order__date_created__gte=CURRENT_MONTH)

        elif filter_by == "year":
            order_items = queryset.filter(order__date_created__gte=CURRENT_YEAR)
        
        else:
            order_items = Order_item.objects

        best_seller = order_items.values('product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        if best_seller:
            response_data = list(best_seller)
            return Response(response_data, status=HTTP_200_OK)
        else:
            response_data = {
                'message': 'No sales data available.'
            }
            return Response(response_data, status=HTTP_404_NOT_FOUND)


class SalesProfitListView(APIView):
    """
    View to calculate and retrieve the total profit from completed sales.

    This view supports the GET HTTP method to retrieve the total profit from completed
    orders. The profit can be filtered based on a specific time range or period, such as
    week, month, or year. Additionally, a custom date range can be specified.

    Methods:
        get(request):
            Calculate and return the total profit from completed orders based on the specified filter.
    """

    def get(self, request):
        """
        Calculate and return the total profit from completed orders.

        This method filters completed orders based on the provided filter parameters
        (`week`, `month`, `year`) or a custom date range (`start_date`, `end_date`).
        It then calculates the profit for these orders and returns the total profit.

        Query Parameters:
            filter (str, optional): A time period filter. Can be one of 'week', 'month', or 'year'.
            start_date (str, optional): The start date for a custom date range, in 'YYYY-MM-DD' format.
            end_date (str, optional): The end date for a custom date range, in 'YYYY-MM-DD' format.

        Args:
            request (HttpRequest): The HTTP request object containing filter parameters.

        Returns:
            Response:
                - A Response object containing the total profit and a status of `HTTP_200_OK` 
                  if profit data is available.
                - A Response object containing a message indicating no sales data is available 
                  and a status of `HTTP_404_NOT_FOUND` if no profit data matches the filter.
        """
        queryset = Order.objects.filter(status="completed")

        filter_by = request.query_params.get("filter", None)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            queryset = queryset.filter(date_created__gte=start_date, date_created__lte=end_date)

        if filter_by:
            if filter_by == "week":
                queryset = queryset.filter(date_created__gte=CURRENT_WEEK)
            elif filter_by == "month":
                queryset = queryset.filter(date_created__gte=CURRENT_MONTH)
            elif filter_by == "year":
                queryset = queryset.filter(date_created__gte=CURRENT_YEAR)
        else:
            queryset = queryset.filter(date_created__exact=TODAY)

        profit = 0
        completed_orders = queryset
        order_items = Order_item.objects.filter(order__in=completed_orders)

        for item in order_items:
            profit += float(item.amount - item.value)
            
        if profit:
            response_data = {
                "profit": profit
            }
            return Response(response_data, status=HTTP_200_OK)
        else:
            response_data = {
                'message': 'No sales data available.'
            }
            return Response(response_data, status=HTTP_404_NOT_FOUND)

        
class ExportOrdersToCsv(APIView):

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="Order_History.csv"'

        writer = csv.writer(response)
        writer.writerow(["date_created", "order_items", "payment_method", "total_amount", "status"])

        data = Order.objects.all().values_list("date_created", "order_items", "payment_method", "total_amount", "status")

        for row in data:
            writer.writerow(row)

        return response


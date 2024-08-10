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

    def get(self, request):
        data = Expenses.objects.all()
        serializer = ExpenseSerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ExpensesCreateView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({"message":"invalid input"}, status=HTTP_400_BAD_REQUEST)


class ExpensesDetailView(APIView):

    def get(self, request, pk):
        data = get_object_or_404(Expenses, pk)
        serializer = ExpenseSerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, pk):
        data = get_object_or_404(Expenses, pk)
        serializer = ExpenseSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response({"message":"invalid input"}, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        data = get_object_or_404(Expenses, pk)
        data.delete()
        return Response({"message": "deleted successfully"}, status=HTTP_200_OK)
    

class StoreCreateApiView(APIView):

    def get(self, request):
        data = Store.objects.all()
        serializer = StoreSrializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = StoreSrializer(data=request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({"message": "invalid input"}, status=HTTP_400_BAD_REQUEST)
        

class ExpenseCategoryListView(APIView):

    def get(self, request):
        data = Expense_category.objects.all()
        serializer = Expense_categorySerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        serializer = Expense_categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        

class ExpenseCategoryDetailView(APIView):

    def get(self, request, pk):
        data = get_object_or_404(Expense_category, pk)
        serializer = Expense_categorySerializer(data)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request, pk):
        data = get_object_or_404(Expense_category, pk)
        serializer = Expense_categorySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        else:
            return Response({"message":"invalid input"}, status=HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        data = get_object_or_404(Expense_category, pk)
        data.delete()
        return Response({"message": "deleted successfully"}, status=HTTP_200_OK)

        

# class BestSellerListView(APIView):

#     def get(self, request):
#         order_items = Order_item.objects.all()
#         for item in order_items:



# class StockLevelAlertView(APIView):
#     products = Product.objects.all()
#     low_stock_level = []

#     for product in products:
#         if product.quantity < 5:
#             low_stock_level += product
    

        
class BestSellingProductView(APIView):
    def get(self, request, format=None):
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

    def get(self, request):

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
            profit += float( item.amount - item.value )
            
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


from rest_framework.status import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expenses
from .serializers import *

# Create your views here.

class ExpensesListView(APIView):

    def get(self, request):
        data = Expenses.objects.all()
        serializer = ExpenseSerializer(data, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
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

        
        
        


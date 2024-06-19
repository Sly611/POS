from .models import *
from rest_framework import serializers


class StoreSrializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ['__all__']
        

class Expense_categorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense_category
        fields = ['__all__']


class ExpenseSerializer(serializers.ModelSerializer):
    category = Expense_categorySerializer()

    class Meta:
        model = Expenses
        fields = ['title', 'description', 'category', 'amount']
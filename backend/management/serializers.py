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
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Expenses
        fields = ['title', 'description', 'category', 'amount']

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category, created = Expense_category.objects.get_or_create(name=category_name)
        expense = Expenses.objects.create(category=category, **validated_data)

        return expense
from rest_framework import serializers
from .models import Product, Category, Payment, Order, Status, Order_item




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['name']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'upc', 'size', 'quantity', 'cost', 'price' ]


class OrderSerializer(serializers.ModelSerializer):
    payment_method = PaymentSerializer()
    status = StatusSerializer()
    class Meta:
        model = Order
        fields = ['id', 'date_created', 'payment_method', 'total_price', 'status']


class Order_itemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    order = OrderSerializer()
    class Meta:
        model = Order_item
        fields = ['order', 'product', 'quantity', 'amount']


from rest_framework import serializers
from .models import Product, Category, Payment, Order, Order_item




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'upc', 'size', 'quantity', 'cost', 'price' ]

    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category, created = Category.objects.get_or_create(name=category_name['name'])
        product = Product.objects.create(category=category, **validated_data)
        return product

class Order_itemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    
    class Meta:
        model = Order_item
        fields = ['product', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField(source='payment_method.name')
    order_items = Order_itemSerializer(many=True)
    # date_created = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Order
        fields = ['id', 'date_created', 'order_items', 'payment_method', 'total_amount', 'status']

    
    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        payment_method_name = validated_data.pop('payment_method')
        payment_method = Payment.objects.get(name=payment_method_name['name'])
        order = Order.objects.create(payment_method=payment_method, **validated_data)
        for item in order_items:
            product_name = item.pop('product')
            product = Product.objects.get(name=product_name['name'])
            Order_item.objects.create(order=order, product=product, **item)
        return order




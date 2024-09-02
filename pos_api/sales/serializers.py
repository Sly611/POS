from rest_framework import serializers
from .models import Product, Category, Payment, Order, Order_item

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer handles the serialization and deserialization of Category
    instances. It includes fields for the Category's ID and name.
    """
    class Meta:
        model = Category
        fields = ['id', 'name']


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.

    This serializer handles the serialization and deserialization of Payment
    instances. It includes fields for the Payment's ID, name, and description.
    """
    class Meta:
        model = Payment
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer handles the serialization and deserialization of Product
    instances. It includes fields for the Product's ID, name, category (represented
    by its name), UPC, size, quantity, cost, and price.

    Custom behavior:
        - Converts the category field to its name representation.
        - Handles creation of Product instances, including category creation if necessary.
    """
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'upc', 'size', 'quantity', 'cost', 'price', 'last_restocked']

    def create(self, validated_data):
        """
        Create a new Product instance.

        Handles the creation of a Product instance, including fetching or creating
        the associated Category based on the provided category name.

        Args:
            validated_data (dict): Data validated by the serializer.

        Returns:
            Product: The created Product instance.
        """
        category_name = validated_data.pop("category")
        category, created = Category.objects.get_or_create(name=category_name['name'])
        product = Product.objects.create(category=category, **validated_data)
        return product


class Order_itemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order_item model.

    This serializer handles the serialization and deserialization of Order_item
    instances. It includes fields for the Order_item's product (represented by its name),
    quantity, and amount.
    """
    product = serializers.CharField(source='product.name')

    class Meta:
        model = Order_item
        fields = ['product', 'quantity', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer handles the serialization and deserialization of Order instances.
    It includes fields for the Order's ID, date created, order items, payment method 
    (represented by its name), total amount, and status.

    Custom behavior:
        - Converts the payment method field to its name representation.
        - Handles creation of Order instances, including fetching the associated Payment 
          and creating related Order_item instances.
    """
    payment_method = serializers.CharField(source='payment_method.name')
    order_items = Order_itemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date_created', 'order_items', 'payment_method', 'total_amount', 'status']

    def create(self, validated_data):
        """
        Create a new Order instance.

        Handles the creation of an Order instance, including fetching the associated 
        Payment based on its name and creating related Order_item instances.

        Args:
            validated_data (dict): Data validated by the serializer.

        Returns:
            Order: The created Order instance.
        """
        order_items = validated_data.pop('order_items')
        payment_method_name = validated_data.pop('payment_method')
        payment_method = Payment.objects.get(name=payment_method_name['name'])
        order = Order.objects.create(payment_method=payment_method, **validated_data)
        for item in order_items:
            product_name = item.pop('product')
            product = Product.objects.get(name=product_name['name'])
            Order_item.objects.create(order=order, product=product, **item)
        return order

from .models import *
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for the Staff model.

    This serializer automatically generates fields for all attributes of the Staff model.
    
    Attributes:
        Meta (class): Meta class for StaffSerializer.
            - model (Model): The model associated with this serializer (Staff).
            - fields (list): A list of model fields to be included in the serialized output. 
              Here, all fields of the Staff model are included.
    """
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'email', 'gender', 'phone', 'address', 'salary', 'role', 'date_joined']


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Store model.

    This serializer handles the serialization and deserialization of Store
    instances. All fields from the Store model are included.
    """
    class Meta:
        model = Store
        fields = ['__all__']


class Expense_categorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense_category model.

    This serializer handles the serialization and deserialization of 
    Expense_category instances. All fields from the Expense_category model 
    are included.
    """
    class Meta:
        model = Expense_category
        fields = ['id', 'name']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expenses model.

    This serializer handles the serialization and deserialization of 
    Expenses instances. It includes fields for the title, description, 
    category (represented by its name), and amount. 

    Custom behavior:
        - Converts the category field to its name representation.
        - Handles creation of Expenses instances, including category creation 
          if necessary.
    """
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Expenses
        fields = ['title', 'description', 'category', 'amount']

    def create(self, validated_data):
        """
        Create a new Expenses instance.

        Handles the creation of an Expenses instance, including fetching or 
        creating the associated Expense_category based on the provided category name.

        Args:
            validated_data (dict): Data validated by the serializer.

        Returns:
            Expenses: The created Expenses instance.
        """
        # Extract category name from validated data
        category_name = validated_data.pop("category") 
        # Retrieve or create the Expense_category instance based on the category name
        category, created = Expense_category.objects.get_or_create(name=category_name)
        # Create the Expenses instance with the validated data
        expense = Expenses.objects.create(category=category, **validated_data)
        
        return expense

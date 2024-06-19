from django.db import models

# Create your models here.

class Store(models.Model):
    bussines_name = models.CharField(max_length=64)
    business_email = models.EmailField()
    address = models.CharField(max_length=256)
    open_hours = models.CharField(max_length=256)

    def __str__(self):
        return self.bussines_name
    

class Expense_category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name
    
    def get_category_expenses(self):
        return self.category_expenses.all()

    
class Expenses(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=526)
    category = models.ForeignKey(Expense_category, on_delete=models.CASCADE, related_name="category_expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} amount: {self.amount}"
    
    






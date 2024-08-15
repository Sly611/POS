from django.db import models
from django.shortcuts import get_object_or_404
from sales.models import Product
# Create your models here.

def store_logo_upload_path(filename):
    return f"logo/{filename}"


class Store(models.Model):
    bussines_name = models.CharField(max_length=64)
    business_email = models.EmailField()
    address = models.CharField(max_length=256)
    open_hours = models.CharField(max_length=256)
    logo = models.FileField(upload_to=store_logo_upload_path,null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            prev = get_object_or_404(Store, id=self.id)
            if prev.logo != self.logo:
                prev.logo.delete(save=False)
                super(Store, self).save(*args, **kwargs)
            


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
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} amount: {self.amount}"
    

class StockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_stock_alert")
    level = models.IntegerField()

    
    
    
    






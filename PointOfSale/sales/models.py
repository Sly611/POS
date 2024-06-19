from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

    

class Category(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_category_products(self):
        return self.category_products.all()
    

class Status(models.Model):
    name = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(Status, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_status_orders(self):
        return self.order_status.all()
    

class Payment(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(Payment, self).save(*args, **kwargs)    

    def __str__(self):
        return self.name
    
    def get_payment_orders(self):
        return self.payment_orders.all()


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING , related_name='category_products')
    upc = models.CharField(max_length=13, unique=True)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(name='cost', max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(name='price', max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField( null=False, blank=False, max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, related_name='payment_orders')
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='order_status')
    
    def __str__(self):
        return str(self.date_created)
    
    def get_order_items(self):
        return self.order_items.all()


class Order_item(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_order')
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)    

    def save(self, *args, **kwargs):
        if self.quantity:
            self.product.quantity -= self.quantity
            self.product.save()
        super(Order_item, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.product} Qty:{self.quantity} price:{self.amount}"

    def update_product_qty(self):
        self.product.quantity += self.quantity
        self.product.save()


@receiver(post_save, sender=Order)
def update_product(sender, instance, **kwargs):
    if instance.status.name == 'cancelled':
        order_items = instance.get_order_items()
        for item in order_items:
            item.update_product_qty()

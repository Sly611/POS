from django.db import models
from django.db.models.signals import post_save, pre_save
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
    

class CancelledOrdersTracker(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"date: {self.date} & time: {self.time}"


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
    upc = models.CharField(max_length=13, unique=True, null=True, blank=True)
    size = models.CharField(max_length=5)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(name='cost', max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(name='price', max_digits=10, decimal_places=2)
    last_restocked = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_status = (
        ("completed", "completed"),
        ("pending", "pending"),
        ("cancelled", "cancelled")
    )
    date_created = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField( default=0, null=False, blank=False, max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(Payment, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='payment_orders')
    status = models.CharField(max_length=64, default="pending", choices=order_status, blank=True, null=True)

    def get_order_items(self):
        return self.order_items.all()
              
    def __str__(self):
        return str(self.date_created)


class Order_item(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_order')
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    value = models.DecimalField( default=0, max_digits=10, decimal_places=2)

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


@receiver(pre_save, sender=Order_item)
def update_total_price(sender, instance, **kwargs):
    # instance.profit = instance.product
    if not instance.amount:
        product_price = instance.product.price
        product_cost = instance.product.cost
        instance.amount = product_price * instance.quantity
        instance.value = product_cost * instance.quantity


@receiver(post_save, sender=Order)
def update_product(sender, instance, **kwargs):
    if instance.status == 'cancelled':
        order_items = instance.get_order_items()
        for item in order_items:
            item.update_product_qty()

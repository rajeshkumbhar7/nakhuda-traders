from django.db import models
from django.utils import timezone
import uuid

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=True,
                                     blank=True)
    selling_price = models.DecimalField(max_digits=10,
                                        decimal_places=2,
                                        null=True,
                                        blank=True)
    stock = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class Cart(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.name



class Customer(models.Model):
    userid = models.CharField(max_length=36, default=uuid.uuid4)
    invnumber = models.IntegerField(null=True)
    customer_name = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=15)
    payment_mode = models.CharField(max_length=10)
    cart_items = models.ManyToManyField(Cart)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer_name

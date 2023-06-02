from products.models import Product
from users.models import User
from django.db import models


class Order(models.Model):
    order_id = models.CharField(max_length=10, blank=False, null=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    products = models.ManyToManyField(to=Product, through="OrderProduct", related_name="orders")
    shipping_fee = models.PositiveIntegerField(default=0, blank=True, null=False)


class OrderProduct(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    color = models.CharField(
        max_length=10, choices=Product.Color.choices, blank=False, null=False
    )
    size = models.PositiveSmallIntegerField(blank=False, null=False)
    quantity = models.PositiveSmallIntegerField(blank=False, null=False)

    class Meta:
        unique_together = ["order", "product", "color", "size"]


class Payment(models.Model):
    order = models.OneToOneField(to=Order, related_name="payment", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=False, null=False)
    transaction_id = models.UUIDField(blank=False, null=False)
    transaction_code = models.PositiveSmallIntegerField(blank=True, null=True)
    shaparak_reference_id = models.CharField(max_length=15, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)

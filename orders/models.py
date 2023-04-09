from products.models import Product
from users.models import User
from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(to=Product)


class Payment(models.Model):
    order = models.OneToOneField(
        to=Order,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        blank=False,
        null=False,
    )
    datetime = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
    )
    transaction_number = models.PositiveIntegerField(
        blank=False,
        null=False,
    )

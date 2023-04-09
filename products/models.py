from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    type = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    brand = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    size = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
    )
    price = models.PositiveIntegerField(
        blank=False,
        null=False,
    )
    color = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )

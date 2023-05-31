from django.db import models


class Product(models.Model):
    class ProductGender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        BOTH = "both"

    class Brand(models.TextChoices):
        SKECHERS = "Skechers"
        ADIDAS = "Adidas"
        ASICS = "ASICS"
        GUCCI = "Gucci"
        NIKE = "Nike"
        PUMA = "Puma"
        VANS = "Vans"

    class Color(models.TextChoices):
        BLACK = "black"
        WHITE = "white"
        GREEN = "green"
        BLUE = "blue"
        RED = "red"

    class Type(models.TextChoices):
        RUNNING = "running"
        HIKING = "hiking"
        SOCCER = "soccer"
        SPORT = "sport"
        BOOT = "boot"

    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    brand = models.CharField(
        max_length=10,
        choices=Brand.choices,
        blank=False,
        null=False,
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        blank=False,
        null=False,
    )
    price = models.PositiveIntegerField(
        blank=False,
        null=False,
    )
    details = models.JSONField(
        default={},
        blank=True,
        null=False,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=6,
        choices=ProductGender.choices,
        blank=False,
        null=False,
    )
    images = models.JSONField(
        default={},
        blank=True,
        null=False,
    )
    # TODO: Rating


class Comment(models.Model):
    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    message = models.TextField(
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False,
    )

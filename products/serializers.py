from django.core.validators import RegexValidator
from rest_framework import serializers
from products import models
from typing import Dict


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"

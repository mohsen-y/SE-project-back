from django.core.validators import RegexValidator
from rest_framework import serializers
from users import models
from typing import Dict


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex="^9\d{9}$",
                message=(
                    "Enter a valid value. This value may contain numbers only, "
                    "and must be exactly 10 digits starting with '9'"
                ),
            )
        ],
        allow_null=True,
    )
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password_confirm = serializers.CharField(min_length=8, write_only=True, required=True)

    def validate_email(self, email: str) -> str:
        if models.User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError(
                detail="A user is already registered with this email address."
            )
        return email

    def validate_phone(self, phone: str) -> str:
        if models.User.objects.filter(phone__exact=phone).exists():
            raise serializers.ValidationError(
                detail="A user is already registered with this phone number."
            )
        return phone

    def validate(self, data: Dict) -> Dict:
        if not data.get("email", None) and not data.get("phone", None):
            raise serializers.ValidationError(
                detail="Enter either a valid email address or phone number to register."
            )
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                detail="Passwords do not match."
            )
        return data

    def create(self, validated_data: Dict) -> models.User:
        validated_data.pop("password_confirm")
        return models.User.objects.create_user(**validated_data)

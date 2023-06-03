from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from users import models
from typing import Dict


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_password(self, password: str) -> str:
        validate_password(password=password)
        return password

    def validate(self, data: Dict) -> Dict:
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                detail="Passwords do not match."
            )
        return data


class UserCreateSerializer(ChangePasswordSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True, allow_null=False)
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
    role = serializers.ChoiceField(choices=models.User.Role.choices, required=False)

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

    def create(self, validated_data: Dict) -> models.User:
        validated_data.pop("password_confirm")
        return models.User.objects.create_user(**validated_data)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = [
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        ]
        read_only_fields = ["id"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = [
            "last_login",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "date_joined",
            "role",
        ]
        read_only_fields = ["id"]

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)

        self.fields["email"].required = False


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_null=False)


class ResetPasswordSerializer(ChangePasswordSerializer, SendOTPSerializer):
    code = serializers.CharField(required=True)

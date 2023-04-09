from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserManager(DefaultUserManager):
    use_in_migrations = True

    def _create_user(self, password, email=None, phone=None, **extra_fields):
        """
        Create and save a user with the given email, phone, and password.
        """
        if not email and not phone:
            raise ValueError("One of the email or phone must be set")
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password=password, email=email, phone=phone, **extra_fields)

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(password=password, email=email, phone=phone, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "O", "Owner"
        ADMIN = "A", "Admin"
        CUSTOMER = "C", "Customer"
    
    username = None
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        verbose_name="phone number",
        max_length=10,
        validators=[
            RegexValidator(
                regex="^9\d{9}$",
                message=(
                    "Enter a valid value. This value may contain numbers only, "
                    "and must be exactly 10 digits starting with '9'"
                ),
            )
        ],
        unique=True,
        blank=True,
        null=True,
    )
    address = models.CharField(
        verbose_name="address",
        max_length=255,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=1,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from config import settings


class UserManager(DefaultUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, phone=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, phone=phone, **extra_fields)

    def create_superuser(self, email=None, password=None, phone=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email=email, password=password, phone=phone, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "owner"
        ADMIN = "admin"
        CUSTOMER = "customer"

    username = None
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        blank=False,
        null=False,
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
        max_length=1023,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=8,
        choices=Role.choices,
        default=Role.CUSTOMER,
        blank=False,
        null=False,
    )
    zip_code = models.CharField(
        verbose_name="zip code",
        max_length=15,
        unique=True,
        blank=True,
        null=True,
    )
    national_id = models.CharField(
        verbose_name="national ID",
        max_length=15,
        unique=True,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class OTP(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False)
    code = models.CharField(max_length=6, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False, name=False)

    def is_valid(self):
        return ((timezone.now() - self.updated_at).seconds / 60) < settings.OTP_EXPIRES_MINUTES

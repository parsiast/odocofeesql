from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phonenumber = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "phonenumber"]

    objects = CustomerManager()

    def __str__(self):
        return self.username


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    locationame = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.locationame} - {self.customer.username}"

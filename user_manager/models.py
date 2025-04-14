from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from base.models import BaseModel, Country, State


class CustomUser(AbstractBaseUser, BaseModel):
    """
    Custom user model that extends AbstractUser.
    """
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # Add any additional fields you want here

class UserWallet(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Shows the available balance from billing service
    account_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    wallet_currency = models.CharField(max_length=20, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)


class Identity(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    source_ip = models.CharField(max_length=20, blank=True, null=True)
    expiry = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
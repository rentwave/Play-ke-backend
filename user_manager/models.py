from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from base.models import BaseModel, Country, State, GenericBaseModel


class Role(GenericBaseModel):
    """
    Model representing the role of a document.
    """
    def __str__(self):
        return self.name

class Permission(GenericBaseModel):
    """
    Model representing the permission of a document.
    """
    def __str__(self):
        return self.name


class RolePermission(GenericBaseModel):
    """
        Model representing the role permission of a document.
        """
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, blank=True, null=True, on_delete=models.CASCADE)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.CASCADE)


class CustomUser(AbstractBaseUser, BaseModel):
    """
    Custom user model that extends AbstractUser.
    """
    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'user_name'

    def __str__(self):
        return '%s' % self.full_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserWallet(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Shows the available balance from billing service
    account_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    wallet_currency = models.CharField(max_length=20, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % self.balance


class Identity(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    source_ip = models.CharField(max_length=20, blank=True, null=True)
    expiry = models.DateField(null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % self.source_ip
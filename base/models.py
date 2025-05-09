import random
import string
import uuid

from django.db import models

# Create your models here.

class BaseModel(models.Model):
    """
    Abstract base model that includes common fields for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class GenericBaseModel(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta(object):
        """Meta"""
        abstract = True


class State(GenericBaseModel):
    """
    Model representing the state of a document.
    """
    def __str__(self):
        return self.name


class Country(BaseModel):
    """
    Model representing a country.
    """
    def __str__(self):
        return self.created_at


class SystemClient(GenericBaseModel):
    consumer_key = models.CharField(max_length=255, unique=True)
    consumer_secret = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def regenerate_credentials(self):
        alphabet = string.ascii_letters + string.digits
        self.consumer_key = ''.join(random.choices(alphabet, k=16))
        raw_secret = ''.join(random.choices(alphabet, k=32))
        self.consumer_secret_raw = raw_secret
        self.consumer_secret = raw_secret
        self.save()
        return raw_secret
    
    def save(self, *args, **kwargs):
        if not self.consumer_key or not self.consumer_secret:
            self.regenerate_credentials()
        super().save(*args, **kwargs)


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

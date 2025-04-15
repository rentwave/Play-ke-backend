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


class State(BaseModel):
    """
    Model representing the state of a document.
    """
    pass

    def __str__(self):
        return self.name


class Country(BaseModel):
    """
    Model representing a country.
    """
    def __str__(self):
        return self.name

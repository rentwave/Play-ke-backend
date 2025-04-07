from base.backend.servicebase import ServiceBase

from user_manager.models import *

class IdentityService(ServiceBase):
    """
    Service class for Identity Model
    """
    manager = Identity.objects


from base.backend.servicebase import ServiceBase

from base.models import *

class StateService(ServiceBase):
    """
    Service class for Identity Model
    """
    manager = State.objects


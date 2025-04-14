from django.urls import re_path, include
from user_manager.api.user_manager import UserManagement

urlpatterns = [
    re_path(r'^auth/', include('user_manager.views'), name='authentication'),
]
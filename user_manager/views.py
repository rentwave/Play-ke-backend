from django.http import JsonResponse
from django.shortcuts import render
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from common.utils import get_request_data
from user_manager.api.user_manager import UserManagement


# Create your views here.
@csrf_exempt
def onboard_user(request):
    """The method to onboard the user"""
    try:
        data = get_request_data(request)
        return JsonResponse(UserManagement().create_user(**data))
    except Exception as e:
        print('create user View Exception: %s', e)
    return JsonResponse({"code": "100.000.003"})

@csrf_exempt
def auth_user(request):
    try:
        data = get_request_data(request)
        return JsonResponse(UserManagement().authenticate_user(**data))
    except Exception as e:
        print('create user View Exception: %s', e)
    return JsonResponse({"code": "100.000.003"})

urlpatterns = [
    re_path(r'^onboard/$', onboard_user),
    re_path(r'^authenticate/$', auth_user),
]

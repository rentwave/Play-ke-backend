import json
from functools import wraps
from django.http import JsonResponse
from django.utils import timezone
from base.models import SystemClient
from common.utils import get_request_data
from django.core.handlers.wsgi import WSGIRequest


def auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        request = None
        for k in args:
            print("args", k)
            if isinstance(k, WSGIRequest):
                request = k
                break
        if not request:
            return JsonResponse({'error': 'Request object not found.'}, status=500)
        request_data = get_request_data(request)
        token = request_data.get("token", False)
        if token is False:
            auth_header = str(request.headers.get('Authorization', ""))
            token = auth_header[len("Bearer "):] if auth_header.startswith("Bearer ") else auth_header
        if not token:
            return JsonResponse({'error': 'Missing or invalid Authorization token.'}, status=401)
        try:
            client = SystemClient.objects.get(access_token=token, is_active=True)
        except SystemClient.DoesNotExist:
            return JsonResponse({'error': 'Invalid or expired token. Use: /auth/token/'}, status=401)
        if client.token_expiry < timezone.now():
            client.is_active = False
            client.save()
            return JsonResponse({'error': 'Token expired. Use: /auth/token/'}, status=401)
        request.system_client = client
        return view_func(*args, **kwargs)
    return _wrapped_view

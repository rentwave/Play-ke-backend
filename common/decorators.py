from functools import wraps
from django.http import JsonResponse
from django.utils import timezone
from base.models import SystemClient

def auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith("Bearer "):
            return JsonResponse({'error': 'Missing or invalid Authorization header. Use: /auth/token/'}, status=401)
        token = auth_header[len("Bearer "):]
        try:
            client = SystemClient.objects.get(access_token=token, is_active=True)
        except SystemClient.DoesNotExist:
            return JsonResponse({'error': 'Invalid or expired token. Use: /auth/token/'}, status=401)
        if client.token_expiry < timezone.now():
            client.is_active = False
            client.save()
            return JsonResponse({'error': 'Token expired. Use: /auth/token/'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

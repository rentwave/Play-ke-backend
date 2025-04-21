import json
from functools import wraps
from django.http import JsonResponse
from django.utils import timezone
from base.models import SystemClient

def auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            token = None
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body.decode('utf-8'))
                    token = data.get('token')
                except json.JSONDecodeError:
                    return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
            elif request.content_type.startswith('multipart/form-data') or request.content_type == 'application/x-www-form-urlencoded':
                token = request.POST.get('token')
            if not token:
                return JsonResponse({'error': 'Missing token in request body.'}, status=401)
            try:
                client = SystemClient.objects.get(access_token=token, is_active=True)
            except SystemClient.DoesNotExist:
                return JsonResponse({'error': 'Invalid or expired token.'}, status=401)

            if client.token_expiry < timezone.now():
                client.is_active = False
                client.save()
                return JsonResponse({'error': 'Token expired.'}, status=401)
            request.client = client
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': f'Auth failure: {str(e)}'}, status=500)

    return _wrapped_view

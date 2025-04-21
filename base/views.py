import random
import string
from datetime import timedelta
from django.urls import path
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.models import SystemClient
from common.response_provider import ResponseProvider


@csrf_exempt
def token(request):
	key = request.headers.get('X-Consumer-Key')
	secret = request.headers.get('X-Consumer-Secret')
	if not key or not secret:
		return ResponseProvider(code="404.000", message={'error': 'Missing authentication headers'}).bad_request()
	try:
		client = SystemClient.objects.get(consumer_key=key, is_active=True)
	except SystemClient.DoesNotExist:
		return ResponseProvider(code="401.000", message={'error': 'Invalid consumer key'}).unauthorized()
	if client.consumer_secret != secret:
		return ResponseProvider(code="401.000", message={'error': 'Invalid consumer secret'}).unauthorized()
	alphabet = string.ascii_letters + string.digits
	token = ''.join(random.choices(alphabet, k=40))
	expiry = timezone.now() + timedelta(hours=1)
	client.access_token = token
	client.token_expiry = expiry
	client.save()
	return JsonResponse({
		'access_token': token,
		'expires_at': expiry.isoformat()
	})


urlpatterns = [
	path('token/', token, name='token'),
]

from django.contrib import admin
from base.models import SystemClient

# Register your models here.
@admin.register(SystemClient)
class SystemClientAdmin(admin.ModelAdmin):
	list_display = ('consumer_key', 'consumer_secret', 'access_token', 'token_expiry', 'is_active', 'created_at')
	list_filter = ('is_active', 'created_at')
	search_fields = ('consumer_key', 'access_token')
	readonly_fields = ('created_at', 'updated_at')
	
	actions = ['regenerate_client_secrets']
	
	@admin.action(description="Regenerate client credentials for selected clients")
	def regenerate_client_secrets(self, request, queryset):
		for client in queryset:
			raw_secret = client.regenerate_credentials()
		self.message_user(request, "Client credentials regenerated successfully.")

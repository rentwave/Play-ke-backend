from django.contrib import admin

# Register your models here.
from user_manager.models import CustomUser, UserWallet, Identity

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin Custom User"""
    list_display = ('name', 'bio', 'phone_number', 'created_at', 'email', 'full_name')
    search_fields = ('name',)


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    """Admin Custom User"""
    list_display = ('user', 'balance', 'account_number', 'wallet_currency', 'state', )
    search_fields = ('name', 'user__name')


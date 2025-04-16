from django.contrib import admin

# Register your models here.
from user_manager.models import CustomUser, UserWallet, Identity, Role, Permission, RolePermission

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin Custom User"""
    list_display = ('bio', 'phone_number', 'created_at', 'email', 'full_name')
    search_fields = ('name',)


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    """Admin Custom User"""
    list_display = ('user', 'balance', 'account_number', 'wallet_currency', 'state', )
    search_fields = ('user__full_name',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__name',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)


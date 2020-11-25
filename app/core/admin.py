from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['created_at']
    list_display = ['email', 'first_name', 'last_name', 'created_at']
    readonly_fields = ('id', 'uuid', 'created_at', 'updated_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('id', 'uuid', 'first_name', 'last_name', 'user_name')}),
        (_('Level'), {'fields': ('level',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('created_at', 'updated_at', 'last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)

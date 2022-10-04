from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_superuser', 'is_staff', 'groups'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_display = (
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
    )
    ordering = ('email',)
    search_fields = ('first_name', 'last_name', 'email')


admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authen.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'phone']
    search_fields = ['username',]
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Personal Information', {'fields': ('phone', 'avatar',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


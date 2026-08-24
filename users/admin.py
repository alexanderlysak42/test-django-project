from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    readonly_fields = ('is_staff',)

    fieldsets = UserAdmin.fieldsets + (
        (
            'Role',
            {
                'fields': ('role',)
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Role',
            {
                'fields': ('role',)
            },
        ),
    )



admin.site.register(User, CustomUserAdmin)
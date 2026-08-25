from django.contrib import admin

from projects.models import Project
from users.models import User

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.filter(role=User.Role.MANAGER)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    list_display = (
        'name',
        'client_name',
        'manager',
        'status',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'name',
        'client_name',
        'client_phone',
        'address',
    )

    list_filter = (
        'status',
        'manager'
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    filter_horizontal = (
        'workers',
    )

    fieldsets = (
        (
            'Основная информация',
            {
                'fields': (
                    'name',
                    'description',
                    'status',
                ),
            },
        ),
        (
            'Клиент',
            {
                'fields': (
                    'client_name',
                    'client_phone',
                ),
            },
        ),
        (
            'Объект',
            {
                'fields': (
                    'address',
                ),
            },
        ),
        (
            'Управление',
            {
                'fields': (
                    'manager',
                    'workers',
                ),
            },
        ),
        (
            'Системная информация',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                ),
            },
        ),
    )
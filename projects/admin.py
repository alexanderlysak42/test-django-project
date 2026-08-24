from django.contrib import admin

from projects.models import Project

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
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
from django.db import migrations

TEST_PROJECT_COUNT = 20

STATUSES = ['new', 'in_progress', 'on_hold', 'completed', 'cancelled']


def create_test_projects(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    User = apps.get_model('users', 'User')

    managers = list(User.objects.filter(role='manager'))

    for i in range(1, TEST_PROJECT_COUNT + 1):
        Project.objects.create(
            name=f'Test Project {i}',
            description=f'Auto-generated test project #{i}',
            client_name=f'Test Client {i}',
            client_phone=f'+7900000{i:04d}',
            address=f'Test address {i}',
            manager=managers[(i - 1) % len(managers)] if managers else None,
            status=STATUSES[(i - 1) % len(STATUSES)],
        )


def remove_test_projects(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Project.objects.filter(name__startswith='Test Project ').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_options_20260824135543'),
    ]

    operations = [
        migrations.RunPython(create_test_projects, remove_test_projects),
    ]

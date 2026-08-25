from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_manager_20260824134338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-created_at',)},
        ),
    ]

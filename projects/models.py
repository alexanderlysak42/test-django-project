from django.db import models

# Create your models here.

class Project(models.Model):

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In progress'
        ON_HOLD = 'on_hold', 'On hold'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    name = models.CharField(
        max_length = 255
    )

    description = models.TextField(
        blank = True
    )

    client_name = models.CharField(
        max_length=255
    )

    client_phone = models.CharField(
        max_length=30,
    )

    address = models.CharField(
        max_length = 500,
    )

    manager = models.ForeignKey(
        'users.User',
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'managed_projects',
    )

    workers = models.ManyToManyField(
        'users.User',
        blank=True,
        related_name='projects',
    )

    created_at = models.DateTimeField(
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        auto_now = True,
    )

    status = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.NEW,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)
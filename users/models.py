from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
        WORKER = 'worker', 'Worker'

    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default = Role.WORKER,
    )

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_superuser = True

        self.is_staff = self.is_superuser or self.role == self.Role.ADMIN

        super().save(*args, **kwargs)
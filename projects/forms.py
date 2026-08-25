from django import forms

from projects.models import Project
from users.models import User


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        if user and user.role == User.Role.MANAGER:
            self.fields.pop(
                'manager',
                None,
            )
        elif 'manager' in self.fields:
            self.fields['manager'].queryset = User.objects.filter(role=User.Role.MANAGER)

        if 'workers' in self.fields:
            self.fields['workers'].queryset = User.objects.filter(
                role=User.Role.WORKER,
            )

    class Meta:
        model = Project

        fields = (
            'name',
            'description',
            'client_name',
            'client_phone',
            'address',
            'manager',
            'workers',
            'status',
        )
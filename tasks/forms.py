
from django import forms

from tasks.models import Task
from users.models import User


class TaskForm(forms.ModelForm):

    def __init__(
        self,
        *args,
        project=None,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        if project:
            self.fields['assigned_to'].queryset = project.workers.filter(
                role=User.Role.WORKER,
            )

    class Meta:
        model = Task

        fields = (
            'title',
            'description',
            'assigned_to',
            'status',
        )

from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        if user and user.role == 'manager':
            self.fields.pop(
                'manager',
                None,
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
            'status',
        )
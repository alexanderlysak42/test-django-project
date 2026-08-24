from typing import cast

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from projects.decorators import roles_required
from projects.forms import ProjectForm
from projects.models import Project
from users.models import User


# Create your views here.

@login_required
def projects_list(request):
    projects = Project.objects.order_by('-created_at')

    context = {
        'projects': projects
    }

    return render (
        request,
        'projects/projects_list.html',
        context,
    )

@login_required
@roles_required('admin', 'manager')
def project_create(request):
    user = cast(User, request.user)

    if request.method == 'POST':
        form = ProjectForm(
            request.POST,
            user = user,
        )

        if form.is_valid():
            project = form.save(
                commit = False
            )

            if user.role == 'manager':
                project.manager = user

            project.save()

            return redirect('projects_list')

    else:

        form = ProjectForm(
            user = user,
        )

    context = {
        'form': form
    }

    return render(
        request,
        'projects/project_create.html',
        context,
    )

@login_required
@roles_required('admin', 'manager')
def project_update(request, project_id):
    user = cast(User, request.user)
    project = get_object_or_404(Project, id=project_id,)

    if user.role == 'manager' and project.manager != user:
        return HttpResponseForbidden('You can only edit your own projects.')

    if request.method == 'POST':
        form = ProjectForm(
            request.POST,
            instance = project,
            user = user,
        )

        if form.is_valid():
            form.save()

            return redirect('projects_list')

    else:
        form = ProjectForm(
            instance = project,
            user = request.user,
        )

    context = {
        'form': form,
        'project': project,
    }

    return render(
        request,
        'projects/project_update.html',
        context,
    )

@login_required
@roles_required('admin')
def project_delete(request, project_id):

    project = get_object_or_404(
        Project,
        id = project_id,
    )

    if request.method == 'POST':
        project.delete()

        return redirect('projects_list')

    context = {
        'project': project,
    }

    return render(
        request,
        'projects/project_delete.html',
        context,
    )
from typing import cast
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from projects.models import Project
from projects.utils import get_safe_next_url
from tasks.forms import TaskForm
from tasks.models import Task
from users.models import User


@login_required
def tasks_list(request):
    user = cast(User, request.user)

    search = request.GET.get(
        'search',
        '',
    ).strip()

    status = request.GET.get(
        'status',
        '',
    )

    ordering = request.GET.get(
        'ordering',
        '-created_at',
    )

    project_id = request.GET.get(
        'project',
        '',
    )

    assigned_to = request.GET.get(
        'assigned_to',
        '',
    )

    if user.role == User.Role.ADMIN:
        tasks = Task.objects.all()

        projects = Project.objects.all()

    elif user.role == User.Role.MANAGER:
        tasks = Task.objects.filter(
            project__manager=user,
        )

        projects = Project.objects.filter(
            manager=user,
        )

    else:
        tasks = Task.objects.filter(
            assigned_to=user,
        )

        projects = Project.objects.filter(
            tasks__assigned_to=user,
        ).distinct()

    if user.role == User.Role.ADMIN:
        workers = User.objects.filter(
            role=User.Role.WORKER,
        )

    elif user.role == User.Role.MANAGER:
        workers = User.objects.filter(
            projects__manager=user,
        ).distinct()

    else:
        workers = User.objects.none()

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
        )

    valid_statuses = [
        choice[0]
        for choice in Task.Status.choices
    ]

    if status in valid_statuses:
        tasks = tasks.filter(
            status=status,
        )
    else:
        status = ''

    if project_id and not project_id.isdigit():
        project_id = ''

    if assigned_to and not assigned_to.isdigit():
        assigned_to = ''

    if project_id:
        tasks = tasks.filter(
            project_id=project_id,
        )

    if assigned_to:
        tasks = tasks.filter(
            assigned_to_id=assigned_to,
        )

    allowed_ordering = (
        '-created_at',
        'created_at',
        'title',
        '-title',
    )

    if ordering not in allowed_ordering:
        ordering = '-created_at'

    tasks = tasks.select_related(
        'project',
        'assigned_to',
    ).order_by(
        ordering,
    )

    paginator = Paginator(
        tasks,
        5,
    )

    page_number = request.GET.get(
        'page',
        1,
    )

    page_obj = paginator.get_page(
        page_number,
    )

    query_params = request.GET.copy()

    query_params.pop(
        'page',
        None,
    )

    query_string = query_params.urlencode()

    if query_string:
        query_string += '&'

    context = {
        'projects': projects,
        'workers': workers,
        'search': search,
        'status': status,
        'ordering': ordering,
        'project_id': project_id,
        'assigned_to': assigned_to,
        'page_obj': page_obj,
        'query_params': query_string,
    }

    return render(
        request,
        'tasks/tasks_list.html',
        context,
    )


@login_required
def task_create(request, project_id):
    user = cast(User, request.user)

    project = get_object_or_404(
        Project,
        id=project_id,
    )

    if user.role == User.Role.WORKER:
        return HttpResponseForbidden(
            'You do not have permission to create tasks.'
        )

    if (
        user.role == User.Role.MANAGER
        and project.manager != request.user
    ):
        return HttpResponseForbidden(
            'You do not have permission to create tasks for this project.'
        )

    if request.method == 'POST':
        form = TaskForm(
            request.POST,
            project=project,
        )

        if form.is_valid():
            task = form.save(
                commit=False,
            )

            task.project = project

            task.save()

            return redirect(
                'project_detail',
                project_id=project.id,
            )

    else:
        form = TaskForm(
            project=project,
        )

    context = {
        'form': form,
        'project': project,
    }

    return render(
        request,
        'tasks/task_create.html',
        context,
    )

@login_required
def task_detail(request, project_id, task_id,):
    user = cast(User, request.user)

    task = get_object_or_404(
        Task.objects.select_related(
            'project',
            'assigned_to',
        ),
        id=task_id,
        project_id=project_id,
    )

    if user.role == User.Role.MANAGER:
        if task.project.manager != request.user:
            return HttpResponseForbidden(
                'You do not have permission to view this task.'
            )

    elif user.role == User.Role.WORKER:
        if task.assigned_to != request.user:
            return HttpResponseForbidden(
                'You do not have permission to view this task.'
            )

    next_url = get_safe_next_url(request,)

    context = {
        'task': task,
        'project': task.project,
        'next': next_url,
    }

    return render(
        request,
        'tasks/task_detail.html',
        context,
    )

@login_required
def task_update(request, project_id, task_id):
    user = cast(User, request.user)

    task = get_object_or_404(
        Task.objects.select_related(
            'project',
        ),
        id=task_id,
        project_id=project_id,
    )

    next_url = get_safe_next_url(request,)

    if user.role == User.Role.WORKER:
        return HttpResponseForbidden(
            'You do not have permission to edit tasks.'
        )

    if (
        user.role == User.Role.MANAGER
        and task.project.manager != user
    ):
        return HttpResponseForbidden(
            'You do not have permission to edit this task.'
        )

    if request.method == 'POST':
        form = TaskForm(
            request.POST,
            instance=task,
            project=task.project,
        )

        if form.is_valid():
            form.save()

            task_detail_url = reverse(
                'task_detail',
                kwargs={
                    'project_id': task.project_id,
                    'task_id': task.id,
                },
            )

            if next_url:
                task_detail_url += (
                    '?'
                    + urlencode(
                        {
                            'next': next_url,
                        },
                    )
                )

            return redirect(
                task_detail_url,
            )

    else:
        form = TaskForm(
            instance=task,
            project=task.project,
        )

    context = {
        'form': form,
        'task': task,
        'project': task.project,
        'next': next_url,
    }

    return render(
        request,
        'tasks/task_update.html',
        context,
    )

@login_required
def task_delete(request, project_id, task_id):
    user = cast(User, request.user)

    task = get_object_or_404(
        Task.objects.select_related(
            'project',
        ),
        id=task_id,
        project_id=project_id,
    )

    next_url = get_safe_next_url(request,)

    if user.role == User.Role.WORKER:
        return HttpResponseForbidden(
            'You do not have permission to delete tasks.'
        )

    if (
        user.role == User.Role.MANAGER
        and task.project.manager != user
    ):
        return HttpResponseForbidden(
            'You do not have permission to delete this task.'
        )

    if request.method == 'POST':
        task.delete()

        if next_url:
            return redirect(
                next_url,
            )

        return redirect(
            'project_detail',
            project_id=project_id,
        )

    context = {
        'task': task,
        'project': task.project,
        'next': next_url,
    }

    return render(
        request,
        'tasks/task_delete.html',
        context,
    )

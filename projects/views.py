from typing import cast

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from projects.decorators import roles_required
from projects.forms import ProjectForm
from projects.models import Project
from projects.utils import get_safe_next_url
from tasks.models import Task
from users.models import User


# Create your views here.

@login_required
def projects_list(request):
    user = cast(User, request.user)

    if user.role == User.Role.MANAGER:
        projects = Project.objects.filter(manager=user)

    elif user.role == User.Role.WORKER:
        projects = Project.objects.filter(workers=user)

    else:
        projects = Project.objects.all()

    projects = projects.select_related('manager',).prefetch_related('workers',)


    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    ordering = request.GET.get('ordering','-created_at',)

    if search:
        projects = projects.filter(
            Q(name__icontains=search) |
            Q(client_name__icontains=search) |
            Q(client_phone__icontains=search) |
            Q(address__icontains=search)
        )

    if status:
        projects = projects.filter(status=status)

    allowed_ordering = [
        '-created_at',
        'created_at',
        'name',
        '-name',
    ]

    if ordering not in allowed_ordering:
        ordering = '-created_at'

    projects = projects.order_by(
        ordering,
    )

    paginator = Paginator(projects, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop(
        'page',
        None,
    )

    query_string = query_params.urlencode()

    if query_string:
        query_string += '&'

    context = {
        'search': search,
        'status': status,
        'ordering': ordering,
        'page_obj': page_obj,
        'query_params': query_string,
    }

    return render (
        request,
        'projects/projects_list.html',
        context,
    )

@login_required
@roles_required(User.Role.ADMIN, User.Role.MANAGER)
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

            if user.role == User.Role.MANAGER:
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
@roles_required(User.Role.ADMIN, User.Role.MANAGER)
def project_update(request, project_id):
    user = cast(User, request.user)
    project = get_object_or_404(Project, id=project_id,)

    if user.role == User.Role.MANAGER and project.manager != user:
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
            user = user,
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
@roles_required(User.Role.ADMIN)
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

@login_required
def project_detail(request, project_id):
    user = cast(User, request.user)

    project = get_object_or_404(
        Project.objects.select_related(
            'manager',
        ).prefetch_related(
            'workers',
            Prefetch(
                'tasks',
                queryset=Task.objects.select_related(
                    'assigned_to',
                )
            ),
        ), id=project_id,)

    if user.role == User.Role.MANAGER:
        if project.manager != request.user:
            return HttpResponseForbidden(
                'You do not have permission to view this project.'
            )

    elif user.role == User.Role.WORKER:
        if not project.workers.filter(
            id=request.user.id,
        ).exists():
            return HttpResponseForbidden(
                'You do not have permission to view this project.'
            )

    next_url = get_safe_next_url(request)

    context = {
        'project': project,
        'next': next_url,
    }

    return render(
        request,
        'projects/project_detail.html',
        context,
    )
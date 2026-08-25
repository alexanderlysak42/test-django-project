from django.urls import path

from tasks import views


urlpatterns = [
    path(
        '',
        views.tasks_list,
        name='tasks_list',
    ),
]
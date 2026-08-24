from django.urls import path

from projects import views

urlpatterns = [
    path('', views.projects_list, name = 'projects_list'),
    path('create/', views.project_create, name = 'project_create'),
    path('<int:project_id>/edit/', views.project_update, name = 'project_update'),
    path('<int:project_id>/delete/', views.project_delete, name = 'project_delete',),
]
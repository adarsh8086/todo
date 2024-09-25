from django .urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import mark_as_completed, mark_project_as_completed

urlpatterns=[
    path('', views.project_list, name='project_list'),
    path('projects/<int:project_id>/complete/', mark_project_as_completed, name='mark_project_as_completed'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/export/', views.export_project_summary, name='export_project_summary'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('project/<int:project_id>/complete/', mark_as_completed, name='mark_as_completed'),

]
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name= 'register'),
    path('dashboard', views.dashboard_view, name="dashboard"),
    path('projects/', views.projects_view, name="projects"),
    path('project/<int:pk>', views.project_view, name="project"),
    path('profile/', views.user_view, name="profile"),
    path('<int:pk>', views.delete_task, name="delete"),
    path('project/update/<int:pk>', views.update_project_view, name="updateProject"),
    path('add/', views.newtask_view, name='newTask'),
    path('task/update/<int:pk>', views.update_task, name="updateTask"),
    path('logout/', views.user_logout, name='logout'),
    path('add/project/', views.new_project_view, name='addProject')
]

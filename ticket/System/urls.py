from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard', views.dashboard_view, name="dashboard"),
    path('profile/', views.user_view, name="profile"),
    path('logout/', views.user_logout, name='logout'),
]

# urls for projects
urlpatterns += [
    path('project/update/<int:pk>', views.update_project_view, name="updateProject"),
    path('project/delete/<int:pk>', views.delete_project_view, name="deleteProject"),
    path('project/add/', views.new_project_view, name='addProject'),
    path('projects/', views.projects_view, name="projects"),
    path('project/<int:pk>', views.project_view, name="project"),
]

# urls for tasks
urlpatterns += [
    path('task/update/<int:pk>', views.update_task, name="updateTask"),
    path('task/delete/<int:pk>', views.delete_task, name="deleteTask"),
    path('task/add', views.new_task_view, name='newTask'),
]

# urls for bugs
urlpatterns += [
    path('bug/add/', views.add_bug, name="addBug"),
    path('bug/delete/<int:pk>', views.delete_bug_view, name="deleteBug"),
    path('bugs/update/<int:pk>', views.update_bug, name="updateBug"),
]
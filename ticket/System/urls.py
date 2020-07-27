from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view),
    path('dashboard', views.dashboard_view, name="dashboard"),
    path('projects/', views.projects_view, name="projects"),
    path('project/<int:pk>', views.project_view, name="project"),
    path('profile', views.user_view, name= "profile")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.shortcuts import render
from .models import Project,Task

# Create your views here.


def home_view(request):
    return render(request, "base.html")


def dashboard_view(request):
    total_projects = Project.objects.all().count()
    progress_projects = Project.objects.filter(status="Open").count()
    print(progress_projects)
    project_completed = Project.objects.filter(status="Closed").count()
    tasks = Task.objects.all()
    projects = Project.objects.all()
    return render(request, "dashboard.html",{
        "total_projects": total_projects,
        "Inprogress": progress_projects,
        "Completed" : project_completed,
        "projects": projects,
        "tasks": tasks
    })


def projects_view(request):
    projects = Project.objects.all()
    return render(request, "project.html",{
        "projects": projects
    })

from django.shortcuts import render, redirect
from .models import Project, Task, User
from .forms import CreateUser
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def home_view(request):
    return render(request, "base.html")


def dashboard_view(request):
    total_projects = Project.objects.all().count()
    progress_projects = Project.objects.filter(status="Open").count()
    project_completed = Project.objects.filter(status="Closed").count()
    tasks = Task.objects.all()
    projects = Project.objects.all()
    return render(request, "dashboard.html", {
        "total_projects": total_projects,
        "Inprogress": progress_projects,
        "Completed": project_completed,
        "projects": projects,
        "tasks": tasks
    })


def projects_view(request):
    projects = Project.objects.all()
    return render(request, "project.html", {
        "projects": projects
    })


def project_view(request, pk):
    project = Project.objects.get(id=pk)
    return render(request, "project_detail.html",
                  {
                      "project": project
                  })


def user_view(request):
    user = User.objects.get(id="1")
    return render(request, "profile.html", {
        "user": user
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")


def register_view(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = CreateUser()
    return render(request, "register.html", {
        'form': form
    })

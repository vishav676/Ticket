from django.shortcuts import render, redirect
from .models import Project, Task, customer
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
    task = Task.objects.filter(project=pk)
    print(task)
    return render(request, "project_detail.html",
                  {
                      "project": project
                  })


def user_view(request):
    users = customer.objects.get(id="1")
    mail = users.username.email
    return render(request, "profile.html", {
        "user": users,
        "mail": mail
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        userlogin = authenticate(request, username=username, password=password)
        if userlogin is not None:
            login(request, userlogin)
            return redirect("dashboard")

    return render(request, "login.html")


def register_view(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            print("working")
            form.save()

            email = request.POST.get("email")
            username = request.POST.get('username')

            # customer.objects.create(username=username, email=email)
            return redirect('login')
        else:
            print("not working")
            form = CreateUser()
    return render(request, "register.html", {
        'form': form
    })


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('dashboard')

from django.shortcuts import render, redirect
from .models import Project, Task, customer
from .forms import CreateUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def home_view(request):
    return render(request, "base.html")


@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    total_projects = user.user_projects.count()
    progress_projects = user.user_projects.filter(status="Open").count()
    project_completed = user.user_projects.filter(status="Closed").count()
    tasks = Task.objects.all()
    projects = user.user_projects.all()
    return render(request, "dashboard.html", {
        "total_projects": total_projects,
        "Inprogress": progress_projects,
        "Completed": project_completed,
        "projects": projects,
        "tasks": tasks
    })


@login_required(login_url='login')
def projects_view(request):
    projects = Project.objects.all()

    return render(request, "project.html", {
        "projects": projects
    })


@login_required(login_url='login')
def project_view(request, pk):
    project = Project.objects.get(id=pk)
    task = project.projectTasks.all()
    return render(request, "project_detail.html",
                  {
                      "project": project,
                      'tasks': task
                  })


@login_required(login_url='login')
def user_view(request):
    users = customer.objects.get(id="1")
    mail = users.username.email
    return render(request, "profile.html", {
        "user": users,
        "mail": mail
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

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
            return redirect('login')
        else:
            print("not working")
            form = CreateUser()
    return render(request, "register.html", {
        'form': form
    })


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('dashboard')


def newTask_view(request):
    if request.method == "POST":
        name = request.POST.get("title")
        summary = request.POST.get("description")
        project = Project.objects.filter(name=request.POST.get("projectSelect"))[:1].get()
        status = request.POST.get("statusSelect")
        task = Task.objects.create(name=name,summary=summary,project=project, status=status)
        if task is not None:
            task.save()
    user = request.user
    projects = user.user_projects.all()
    status = Task.TASK_STATUS
    return render(request, 'new_task.html',{
        'projects': projects,
        'status': status
    })

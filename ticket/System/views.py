from django.shortcuts import render, redirect
from .models import Project, Task, customer, Bug
from django.contrib.auth.models import Group
from .forms import CreateUser, CustomerForm, CreateProject, task_add_update, BugForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def home_view(request):
    return render(request, "base.html")


@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    total_projects = user.user_projects.count()
    progress_projects = user.user_projects.filter(status="Open").count()
    project_completed = user.user_projects.filter(status="Closed").count()
    all_task = set()
    for task in user.user_projects.select_related('created_by'):
        all_task.add(task.projectTasks.all())
    tasks = all_task
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
    user = request.user
    projects = user.user_projects.all()

    return render(request, "project.html", {
        "projects": projects
    })


@login_required(login_url='login')
def project_view(request, pk):
    project = Project.objects.get(id=pk)
    task = project.projectTasks.all()
    bugs = project.task_bugs.all()
    return render(request, "project_detail.html",
                  {
                      "project": project,
                      'tasks': task,
                      'bugs': bugs
                  })


@login_required(login_url='login')
def user_view(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()

    return render(request, "profile.html", {
        "form": form
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
        else:
            messages.info(request, "Invalid Username or Password.")

    return render(request, "login.html")


def register_view(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group, create = Group.objects.get_or_create(name='customer')
            user.groups.add(group)

            customer.objects.create(user=user, name=user.username)

            return redirect('login')
        else:
            form = CreateUser()
            messages.info(request, "username already exists")
    return render(request, "register.html", {
        'form': form
    })


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('dashboard')


def newtask_view(request):
    form = task_add_update(request.user)
    if request.method == "POST":
        form = task_add_update(request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            form = task_add_update(request.user)
    return render(request, 'add_update.html', {
        'form': form
    })


def new_project_view(request):
    form = CreateProject(request.user)
    if request.method == "POST":
        form = CreateProject(request.user, request.POST)
        print(form)
        if form.is_valid():
            print("working")
            form.save()
        else:
            form = CreateProject(request.user)
    return render(request, 'add_update.html', {
        'form': form
    })


def update_project_view(request, pk):
    project = Project.objects.get(id=pk)
    form = CreateProject(request.user, instance=project)
    if request.method == "POST":
        form = CreateProject(request.user, request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.info(request, "Changes saved")
        else:
            form = CreateProject(request.user, instance=project)

    return render(request, "add_update.html", {
        'form': form
    })


def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = task_add_update(request.user, instance=task)
    if request.method == "POST":
        form = task_add_update(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
        else:
            form = task_add_update(request.user, instance=task)

    return render(request, "add_update.html", {
        "form": form
    })


def add_bug(request):
    form = BugForm(request.user)
    if request.method == "POST":
        form = BugForm(request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            form = BugForm(request.user)

    return render(request, "add_update.html", {
        "form": form
    })


def update_bug(request, pk):
    bug = Bug.objects.get(id=pk)
    form = BugForm(request.user, instance=bug)
    if request.method == "POST":
        form = BugForm(request.user, request.POST, instance=bug)
        if form.is_valid():
            form.save()
        else:
            form = BugForm(request.user, instance=bug)

    return render(request, "add_update.html", {
        "form": form
    })
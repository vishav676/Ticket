from django.shortcuts import render, redirect
from .models import Project, Task, customer, Bug
from django.contrib.auth.models import Group
from .forms import CreateUser, CustomerForm, CreateProject, task_add_update, BugForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.


def home_view(request):
    return render(request, "base.html")


@login_required(login_url='login')
def dashboard_view(request):
    user = request.user
    total_projects = user.user_projects.count()
    progress_projects = user.user_projects.filter(status="Open").count()
    project_completed = user.user_projects.filter(status="Closed").count()
    all_bugs = set()
    all_task = set()
    bugs_reported = 0
    projects = user.user_projects.all()
    for project in projects:
        all_task.add(project.projectTasks.all())
        bugs_reported += project.task_bugs.count()
        all_bugs.add(project.task_bugs.all())
    tasks = all_task
    bugs = all_bugs
    projects_pagination = pagination_view(request, projects, 3)

    return render(request, "dashboard.html", {
        "total_projects": total_projects,
        "Inprogress": progress_projects,
        "Completed": project_completed,
        "projects": projects_pagination,
        "tasks": tasks,
        "bugs": bugs,
        "bugs_reported": bugs_reported
    })


@login_required(login_url='login')
def projects_view(request):
    user = request.user
    projects = user.user_projects.all()

    return render(request, "project.html", {
        "projects": projects
    })


def pagination_view(request, page_class, number):
    paginator = Paginator(page_class, number)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required(login_url='login')
def project_view(request, pk):
    project = Project.objects.get(id=pk)
    task = project.projectTasks.all()
    bugs = pagination_view(request, project.task_bugs.all(), 5)
    page_obj = pagination_view(request, task, 5)

    return render(request, "project_detail.html",
                  {
                      "project": project,
                      'tasks': page_obj,
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
            group, create = Group.objects.get_or_create(name='customer')
            user.groups.add(group)

            customer.objects.create(user=user, name=user.username, email=user.email)

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


@login_required(login_url='login')
def delete_project_view(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    return redirect('projects')


@login_required(login_url='login')
def new_task_view(request):
    form = task_add_update(request.user)
    if request.method == "POST":
        form = task_add_update(request.user, request.POST)
        if form.is_valid():
            form.save()
            form = task_add_update(request.user)
            messages.info(request, "Changes saved")
        else:
            form = task_add_update(request.user)

    return render(request, 'add_update.html', {
        'form': form,
        'title': 'Add New Task'
    })


@login_required(login_url='login')
def new_project_view(request):
    form = CreateProject(request.user)
    if request.method == "POST":
        form = CreateProject(request.user, request.POST)
        print(form)
        if form.is_valid():
            print("working")
            form.save()
            form = CreateProject(request.user)
        else:
            form = CreateProject(request.user)

    return render(request, 'add_update.html', {
        'form': form,
        "title": "Add Project"
    })


@login_required(login_url='login')
def update_project_view(request, pk):
    project = Project.objects.get(id=pk)
    form = CreateProject(request.user, instance=project)
    if request.method == "POST":
        form = CreateProject(request.user, request.POST, instance=project)
        if form.is_valid():
            form.save()
            form = CreateProject(request.user, instance=project)
            messages.info(request, "Changes saved")
        else:
            form = CreateProject(request.user, instance=project)

    return render(request, "add_update.html", {
        'form': form,
        'title': "Update Project"
    })


@login_required(login_url='login')
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = task_add_update(request.user, instance=task)
    if request.method == "POST":
        form = task_add_update(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            form = task_add_update(request.user, instance=task)
        else:
            form = task_add_update(request.user, instance=task)

    return render(request, "add_update.html", {
        "form": form,
        "title": "Update Task"
    })


@login_required(login_url='login')
def add_bug(request):
    form = BugForm(request.user)
    if request.method == "POST":
        form = BugForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            form = BugForm(request.user)
        else:
            form = BugForm(request.user)

    return render(request, "add_update.html", {
        "form": form,
        "title": "Report Bug"
    })


@login_required(login_url='login')
def update_bug(request, pk):
    bug = Bug.objects.get(id=pk)
    form = BugForm(request.user, instance=bug)
    if request.method == "POST":
        form = BugForm(request.user, request.POST, instance=bug)
        if form.is_valid():
            form.save()
            form = BugForm(request.user, instance=bug)
        else:
            form = BugForm(request.user, instance=bug)

    return render(request, "add_update.html", {
        "form": form,
        "title": "Update Bug"
    })


@login_required(login_url='login')
def delete_bug_view(request, pk):
    bug = Bug.objects.get(id=pk)
    bug.delete()
    return redirect('projects')

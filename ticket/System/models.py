from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=50, null=True)
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default="profile.png",null=True,blank=True)

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    PROJECT_STATUS = (
        ("Open", "Open"),
        ("Closed", "Closed")
    )
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=200, choices=PROJECT_STATUS, default="Open", null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_projects')

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    TASK_STATUS = (
        ("Pending", "Pending"),
        ("Progress", "Progress"),
        ("Completed", "Completed")
    )
    name = models.CharField(max_length=50, null=False, blank=False)
    summary = models.TextField(max_length=1000, null=False, blank=False)
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True, related_name='projectTasks')
    date_created = models.DateField(auto_now=True)
    status = models.CharField(max_length=200, choices=TASK_STATUS, default="Pending", null=True)

    def __str__(self):
        return f"{self.name}[{self.project.name}]"


class Bug(models.Model):
    PRIORITY = (
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Normal', 'Normal'),
        ('Low', "Low")
    )
    BUG_STATUS = (
        ("Pending", "Pending"),
        ("Progress", "Progress"),
        ("Completed", "Completed")
    )
    issue = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now=True)
    priority = models.CharField(max_length=50, choices=PRIORITY, default="Normal")
    status = models.CharField(max_length=50, choices=BUG_STATUS, default="Pending")
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='task_bugs')

    def __int__(self):
        return f"{self.issue}[{self.project.name}"

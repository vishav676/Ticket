from django.db import models

# Create your models here.


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

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    TASK_STATUS = (
        ("Pending", "Pending"),
        ("Progress", "Progress"),
        ("Completed", "Completed")
    )
    name = models.CharField(max_length=50)
    summary = models.TextField(max_length=1000)
    project = models.ForeignKey("Project", on_delete=models.SET_NULL, null=True)
    date_created = models.DateField(auto_now=True)
    status = models.CharField(max_length=200, choices=TASK_STATUS, default="Pending", null=True)

    def __str__(self):
        return f"{self.name}----{self.project.name}"


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    emailId = models.EmailField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

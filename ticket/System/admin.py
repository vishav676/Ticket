from django.contrib import admin
from .models import Project, Task, customer, Bug
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(customer)
admin.site.register(Bug)
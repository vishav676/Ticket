from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import customer, Project, Task, Bug
from django import forms
from django.forms import ModelForm, ModelChoiceField


class CreateUser(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        "placeholder": "Email"
    }))
    username = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "username"
    }))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Password"
    }))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Confirm Password"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = customer
        fields = ["email", "name", "profile_pic"]
        exclude = ["user"]


class task_add_update(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(task_add_update, self).__init__(*args, **kwargs)

        try:
            q = Project.objects.filter(created_by=user)
            self.fields['project'] = ModelChoiceField(queryset=q, initial=q, widget=forms.Select(attrs={
                'class': 'form-control'
            }))

        except:
            pass

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    summary = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    status = forms.CharField(widget=forms.Select(choices=Task.TASK_STATUS, attrs={
        'class': 'form-control',
        'style': 'margin-bottom: 10px'
    }))

    class Meta:
        model = Task
        fields = '__all__'


class CreateProject(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(CreateProject, self).__init__(*args, **kwargs)

        try:
            q = User.objects.filter(username=user)
            self.fields['created_by'] = ModelChoiceField(queryset=q, initial=q,widget=forms.Select(attrs={
                'class': 'form-control',
                'style': 'margin-bottom: 10px'
            }))
        except:
            pass

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style': 'margin-bottom: 10px'
    }))
    created_by = forms.CharField(widget=forms.Select(attrs={
        'class': 'form-control',
    }))
    status = forms.CharField(widget=forms.Select(choices=Project.PROJECT_STATUS, attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Project
        fields = ["name", "description", "status","created_by"]


class BugForm(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(BugForm, self).__init__(*args, **kwargs)

        try:
            q = Project.objects.filter(created_by=user)
            self.fields['project'] = ModelChoiceField(queryset=q, initial=q, widget=forms.Select(attrs={
                'class': 'form-control',
                'style': 'margin-bottom: 10px'
            }))
        except:
            pass

    issue = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))
    priority = forms.CharField(widget=forms.Select(choices=Bug.PRIORITY, attrs={
        'class': 'form-control'
    }))
    status = forms.CharField(widget=forms.Select(choices=Bug.BUG_STATUS, attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Bug
        fields = "__all__"

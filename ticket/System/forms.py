from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import customer, Project
from django import forms
from django.forms import ModelForm, ModelChoiceField


class CreateUser(UserCreationForm):
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


class ProjectUpdationForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"


class CreateProject(ModelForm):

    def __init__(self, user, *args, **kwargs):

        super(CreateProject, self).__init__(*args, **kwargs)

        try:
            q = User.objects.filter(username=user)
            self.fields['created_by'] = ModelChoiceField(queryset=q, initial=q)
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

    class Meta:
        model = Project
        fields = ["name", "description", "status", "created_by"]

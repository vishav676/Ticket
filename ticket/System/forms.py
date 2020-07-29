from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import customer
from django.forms import ModelForm


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = customer
        fields = '__all__'
        exclude = ["user"]

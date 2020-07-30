from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import customer, Project
from django.forms import ModelForm, ModelChoiceField


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = customer
        fields = '__all__'
        exclude = ["user"]


class CreateProject(ModelForm):
    def __init__(self, user, *args,**kwargs):
        super(CreateProject, self).__init__(*args,**kwargs)

        try:
            q = User.objects.filter(username=user)
            self.fields['created_by'] = ModelChoiceField(queryset=q, initial=q)
        except:
            pass

    class Meta:
        model = Project
        fields = "__all__"


from django import forms
from .models import EquipmentIssue
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class IssueForm(forms.ModelForm):
    class Meta:
        model = EquipmentIssue
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

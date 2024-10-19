from django.db import models
from django.forms import ModelForm
from django import forms
from django.db.models import Model

# Create your models here.

class UserModel(Model):
    email = models.TextField(unique=True)
    name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=13)
    password = models.CharField(max_length=100)

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserModel
        fields = ['email', 'name', 'contact_number', 'password']

class ExpenseModel(Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    detail = models.CharField(max_length=256)
    expense = models.IntegerField()

class ExpenseForm(ModelForm):
    class meta:
        fields = ['user', 'detail', 'expense']

print(str(ExpenseForm))
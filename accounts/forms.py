from django.forms import forms, ModelForm
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = "username", "email", "password1", "password2"


class OrderForm(ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"
        exclude = "user",

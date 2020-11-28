from django.forms import forms, ModelForm
from . import models


class OrderForm(ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"


class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"


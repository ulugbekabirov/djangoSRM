from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home_view(request):
    return render(request, "accounts/dashboard.html")


def customers_view(request):
    return render(request, "accounts/customers.html")


def products_view(request):
    return render(request, "accounts/products.html")
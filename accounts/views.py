from django.shortcuts import render
from . import models


def home_view(request):
    orders = models.Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    last_five_orders = orders.order_by("-date_created",)[0:5]
    customers = models.Customer.objects.all()
    context = {"orders": orders,
               "total_orders": total_orders,
               "orders_delivered": orders_delivered,
               "orders_pending": orders_pending,
               "last_five_orders": last_five_orders,
               "customers": customers, }
    return render(request, "accounts/dashboard.html", context)


def customers_view(request, customer_id):
    context = {"customer": models.Customer.objects.get(id=customer_id)}
    return render(request, "accounts/customers.html", context)


def products_view(request):
    context = {"products": models.Product.objects.all()}
    return render(request, "accounts/products.html", context)

from django.shortcuts import render, HttpResponseRedirect, redirect
from . import models
from . import forms


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


def create_order_view(request):
    context = {"form": forms.OrderForm}
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")
    return render(request, "accounts/createOrder.html", context)


def create_customer_view(request):
    context = {"form": forms.CustomerForm}
    if request.method == "POST":
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")
    return render(request, "accounts/createCustomer.html", context)


def update_order_view(request, order_id):
    order = models.Order.objects.get(id=order_id)
    if request.method == "POST":
        form = forms.OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            prev_page = request.POST.get('next', '/')
            return HttpResponseRedirect(prev_page)
    context = {
        "order": order,
        "form": forms.OrderForm(instance=order)}
    return render(request, "accounts/updateOrder.html",  context)


def update_customer_view(request, customer_id):
    customer = models.Customer.objects.get(id=customer_id)
    if request.method == "POST":
        form = forms.CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/customer/{}".format(customer_id))
    context = {
        "customer": customer,
        "form": forms.CustomerForm(instance=customer)
    }
    return render(request, "accounts/updateCustomer.html", context)


def delete_order_view(request, order_id):
    order = models.Order.objects.get(id=order_id)
    if request.method == "POST":
        order.delete()
        prev_page = request.POST.get('next', '/')
        return HttpResponseRedirect(prev_page)
    context = {
        "order": order
    }
    return render(request, "accounts/deleteOrder.html", context)
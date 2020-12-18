from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, redirect
from . import models
from . import forms
from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import OrderFilter
from .forms import CreateUserForm, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
@allowed_users(["customer"])
def account_settings_view(request):
    if request.method == "POST":
        form = forms.CustomerForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created")
            return redirect("home")
    context = {"form": CustomerForm(instance=request.user.customer)}
    return render(request, "accounts/account_settings.html", context)


@allowed_users(["customer"])
@login_required(login_url='login')
def user_view(request):
    orders = request.user.customer.order_set.all()
    # print((request.user.email))
    context = {
        "orders": orders,
        "total_orders": orders.count(),
        "orders_delivered": orders.filter(status="Delivered").count(),
        "orders_pending": orders.filter(status="Pending").count(),
    }
    return render(request, "accounts/user.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or Password is incorrect")
            return redirect("login")

    return render(request, "accounts/login.html")


@unauthenticated_user
def register_view(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            models.Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )
            messages.success(request, "Account was created for {}".format(username))
            return redirect("login")

    context = {
        "form": form
    }
    return render(request, "accounts/register.html", context=context)


@login_required(login_url='login')
@admin_only
def home_view(request):
    orders = models.Order.objects.all()
    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    last_five_orders = orders.order_by("-date_created", )[0:5]
    customers = models.Customer.objects.all()
    context = {"orders": orders,
               "total_orders": total_orders,
               "orders_delivered": orders_delivered,
               "orders_pending": orders_pending,
               "last_five_orders": last_five_orders,
               "customers": customers, }
    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
def customers_view(request, customer_id):
    customer = models.Customer.objects.get(id=customer_id)
    orders = customer.order_set.all()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {"customer": customer,
               "orders": orders,
               "my_filter": my_filter, }

    return render(request, "accounts/customers.html", context)


@login_required(login_url='login')
def products_view(request):
    context = {"products": models.Product.objects.all()}
    return render(request, "accounts/products.html", context)


@login_required(login_url='login')
def create_order_view(request):
    context = {"form": forms.OrderForm}
    if request.method == "POST":
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")
    return render(request, "accounts/createOrder.html", context)


@login_required(login_url='login')
def create_customer_view(request):
    context = {"form": forms.CustomerForm}
    if request.method == "POST":
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/")
    return render(request, "accounts/createCustomer.html", context)


@login_required(login_url='login')
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
    return render(request, "accounts/updateOrder.html", context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("customer/<int:customer_id>", views.customers_view, name="customer"),
    path("products", views.products_view, name="products"),
    path("createOrder", views.create_order_view, name="createOrder"),
    path("updateOrder/<int:order_id>", views.update_order_view, name="updateOrder"),
    path("createCustomer", views.create_customer_view, name="createCustomer"),
    path("updateCustomer/<int:customer_id>", views.update_customer_view, name="updateCustomer"),
    path("deleteOrder/<order_id>", views.delete_order_view, name="deleteOrder")
]
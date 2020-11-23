from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("customer/<int:customer_id>", views.customers_view, name="customer"),
    path("products", views.products_view, name="products"),
]
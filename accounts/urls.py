from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("customers", views.customers_view, name="customers"),
    path("products", views.products_view, name="products"),
]
from django.contrib import admin

from . import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "date_created")


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "date_created", "status")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)

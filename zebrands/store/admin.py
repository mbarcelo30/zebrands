from django.contrib import admin

from store.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "brand", "price"]

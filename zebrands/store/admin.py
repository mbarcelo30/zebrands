from django.contrib import admin

from store.models import Product, ProductStats


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["sku", "name", "brand", "price"]


@admin.register(ProductStats)
class ProductStatsAdmin(admin.ModelAdmin):
    list_display = ["product", "view_count"]

from django.contrib import admin

from store.models import Product, ProductStats


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Define the ProductAdmin view to handle the product model in the django admin.
    """

    list_display = ["sku", "name", "brand", "price"]


@admin.register(ProductStats)
class ProductStatsAdmin(admin.ModelAdmin):
    """
    Define the ProductStatsAdmin view to handle the product stats model in the django admin.
    """

    list_display = ["product", "view_count"]

from django.db import models

from model_utils.models import TimeStampedModel

PRODUCT_ADMIN_GROUP = "ProductAdmin"


class Product(TimeStampedModel):
    sku = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=256, null=False)
    price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    brand = models.CharField(max_length=128, null=False)

    def __str__(self):
        return f"{self.sku} - {self.brand} - {self.name}"


class ProductStats(TimeStampedModel):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="stats"
    )
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product} - {self.view_count}"

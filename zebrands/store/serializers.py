from rest_framework import serializers
from store.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("sku", "name")


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        required=True, allow_null=False, max_digits=16, decimal_places=2
    )

    class Meta:
        model = Product
        fields = ("sku", "name", "price", "brand")

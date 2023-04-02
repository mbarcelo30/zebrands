from rest_framework import serializers
from store.models import Product
from store.tasks import product_change_notification


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

    def update(self, instance, validated_data):
        product_change_notification.delay(instance.sku)
        return super(ProductSerializer, self).update(instance, validated_data)

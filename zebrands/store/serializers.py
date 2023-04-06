from rest_framework import serializers
from store.models import Product
from store.tasks import product_change_notification


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer class for the list of products.

    Includes only the 'sku' and 'name' fields.
    """

    class Meta:
        model = Product
        fields = ("sku", "name")


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class for individual products.

    Includes the 'sku', 'name', 'price', and 'brand' fields.
    Performs a Celery task to notify users of product changes upon update.
    """

    price = serializers.DecimalField(
        required=True, allow_null=False, max_digits=16, decimal_places=2
    )

    class Meta:
        model = Product
        fields = ("sku", "name", "price", "brand")

    def update(self, instance, validated_data):
        """
        Performs an update on a product instance, and schedules a Celery task to notify users of changes.

        Args:
        @param instance: The existing product instance to be updated.
        @param validated_data: A dictionary of validated data to be used to update the instance.

        @return: The updated product instance.
        """
        product_change_notification.delay(instance.sku)
        return super(ProductSerializer, self).update(instance, validated_data)

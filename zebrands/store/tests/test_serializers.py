import pytest
from store.serializers import ProductListSerializer, ProductSerializer
from store.tests.factories import ProductFactory

pytestmark = pytest.mark.django_db


def test_product_serializer(product):
    """
    Test the ProductSerializer class by comparing its output with expected values.

    @param product: The product object to serialize.
    @type product: store.models.Product
    """
    # Define the expected output based on the given product object.
    expected = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
    }

    # Create a ProductSerializer instance for the given product object.
    serializer = ProductSerializer(product)

    # Assert that the serialized data matches the expected output.
    assert serializer.data == expected


def test_product_list_serializer():
    """
    Test the ProductListSerializer class by comparing its output with expected values.
    """
    n = 5
    expected = []
    serialized = []

    # Create n product objects using the ProductFactory, and append their expected
    # output and serialized data to their respective lists.
    for i in range(n):
        prod = ProductFactory()
        expected.append({"sku": prod.sku, "name": prod.name})
        serialized.append(ProductListSerializer(prod).data)

    # Assert that the serialized data matches the expected output.
    assert serialized == expected

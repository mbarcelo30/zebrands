import pytest
from store.serializers import ProductListSerializer, ProductSerializer
from store.tests.factories import ProductFactory

pytestmark = pytest.mark.django_db


def test_product_serializer(product):
    expected = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
    }
    serializer = ProductSerializer(product)
    assert serializer.data == expected


def test_product_list_serializer():
    n = 5
    expected = []
    serialized = []
    for i in range(n):
        prod = ProductFactory()
        expected.append({"sku": prod.sku, "name": prod.name})
        serialized.append(ProductListSerializer(prod).data)

    assert serialized == expected

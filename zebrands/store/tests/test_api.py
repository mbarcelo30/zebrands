from django.conf import settings
from django.test import RequestFactory
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from store.models import Product
from store.serializers import ProductListSerializer, ProductSerializer
from store.tests.factories import ProductFactory

pytestmark = pytest.mark.django_db


def test_list_products(user):
    client = APIClient()
    client.force_authenticate(user=user)
    page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 4)
    _ = ProductFactory.create_batch(page_size)

    query = Product.objects.all()
    request_factory = RequestFactory()
    expected_results = ProductListSerializer(
        query, many=True, context={"request": request_factory.get(path="/")}
    ).data

    expected = [status.HTTP_200_OK, expected_results]
    response = client.get(reverse("products-list"))
    received = [response.status_code, response.data]
    assert expected == received


def test_retrieve_product_no_auth(product, mocker):
    client = APIClient()
    expected_results = ProductSerializer(product).data

    expected = [status.HTTP_200_OK, expected_results]
    product_update_counter = mocker.patch("store.views.product_update_counter.delay")
    response = client.get(reverse("products-detail", args=(product.sku,)))
    received = [response.status_code, response.data]

    assert product_update_counter.called
    product_update_counter.assert_called_with(product.sku)
    assert expected == received


def test_retrieve_product_auth(client, product, mocker):
    expected_results = ProductSerializer(product).data
    expected = [status.HTTP_200_OK, expected_results]
    product_update_counter = mocker.patch("store.views.product_update_counter.delay")
    response = client.get(reverse("products-detail", args=(product.sku,)))
    received = [response.status_code, response.data]
    assert not product_update_counter.called
    assert expected == received


def test_create_product_no_group_permission(client, product):
    data = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
    }
    expected = status.HTTP_403_FORBIDDEN
    response = client.post(reverse("products-list"), data=data)
    assert response.status_code == expected


def test_create_product(user, product, mocker):
    client = APIClient()
    client.force_authenticate(user=user)
    data = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
    }
    expected_results = ProductSerializer(product).data
    expected = [status.HTTP_201_CREATED, expected_results]
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)
    response = client.post(reverse("products-list"), data=data)
    received = [response.status_code, response.data]
    assert expected == received


def test_update_product(client, product, mocker):
    data = {
        "name": "test name",
    }
    expected_data = {
        "sku": product.sku,
        "name": "test name",
        "price": str(product.price),
        "brand": product.brand,
    }
    expected_results = expected_data
    expected = [status.HTTP_200_OK, expected_results]
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)
    notify_update_product = mocker.patch(
        "store.serializers.product_change_notification.delay"
    )
    response = client.patch(reverse("products-detail", args=(product.sku,)), data=data)
    received = [response.status_code, response.data]
    assert expected == received
    assert notify_update_product.called
    notify_update_product.assert_called_with(product.sku)


def test_delete_product(client, mocker):
    page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 4)
    prod_list = ProductFactory.create_batch(page_size)
    prod_to_delete = prod_list[1]
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)
    response = client.delete(reverse("products-detail", args=(prod_to_delete.sku,)))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    objects = set(Product.objects.all())
    assert len(objects) == 3
    prod_set = set(prod_list)
    prod_set.remove(prod_to_delete)
    assert prod_set == objects

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
    """
    Test the list_products view function by checking that its response status code and data
    match the expected values.

    @param user: The user to authenticate the client as.
    @type user: django.contrib.auth.models.User
    """
    client = APIClient()
    client.force_authenticate(user=user)
    page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 4)

    # Create a batch of products using the ProductFactory.
    _ = ProductFactory.create_batch(page_size)

    # Retrieve the queryset of all products and create a request factory to be used
    # by the serializer context.
    query = Product.objects.all()
    request_factory = RequestFactory()
    expected_results = ProductListSerializer(
        query, many=True, context={"request": request_factory.get(path="/")}
    ).data

    expected = [status.HTTP_200_OK, expected_results]
    # Send a GET request to the products-list endpoint using the test client, and retrieve
    # the received response as a list containing the HTTP status code and received data.
    response = client.get(reverse("products-list"))
    received = [response.status_code, response.data]

    # Assert that the received response matches the expected response.
    assert expected == received


def test_retrieve_product_no_auth(product, mocker):
    """
    Test the retrieve_product view function without authenticating the client, by checking
    that its response status code and data match the expected values, and that the product's
    update_counter task is called.

    @param product: The product to retrieve.
    @type product: store.models.Product
    @param mocker: The pytest-mock mocker fixture.
    @type mocker: pytest_mock.MockFixture
    """
    client = APIClient()
    expected_results = ProductSerializer(product).data

    expected = [status.HTTP_200_OK, expected_results]

    # Mock the product_update_counter task using the pytest-mock mocker fixture.
    product_update_counter = mocker.patch("store.views.product_update_counter.delay")

    # Send a GET request to the products-detail endpoint for the given product using the test
    # client, and retrieve the received response as a list containing the HTTP status code
    # and received data.
    response = client.get(reverse("products-detail", args=(product.sku,)))
    received = [response.status_code, response.data]

    # Assert that the product_update_counter task was called with the given product's SKU,
    # and that the received response matches the expected response
    assert product_update_counter.called
    product_update_counter.assert_called_with(product.sku)
    assert expected == received


def test_retrieve_product_auth(client, product, mocker):
    """
    Test the retrieve_product view function with an authenticated client, by checking that its
    response status code and data match the expected values, and that the product's update_counter
    task is not called.

    @param client: The test client authenticated with a user.
    @type client: rest_framework.test.APIClient
    @param product: The product to retrieve.
    @type product: store.models.Product
    @param mocker: The pytest-mock mocker fixture.
    @type mocker: pytest_mock.MockFixture
    """
    expected_results = ProductSerializer(product).data
    expected = [status.HTTP_200_OK, expected_results]

    # Mock the product_update_counter task using the pytest-mock mocker fixture.
    product_update_counter = mocker.patch("store.views.product_update_counter.delay")

    # Send a GET request to the products-detail endpoint for the given product using the
    # authenticated test client, and retrieve the received response as a list containing the
    # HTTP status code and received data.
    response = client.get(reverse("products-detail", args=(product.sku,)))
    received = [response.status_code, response.data]

    # Assert that the product_update_counter task was not called, and that the received response
    # matches the expected response.
    assert not product_update_counter.called
    assert expected == received


def test_create_product_no_group_permission(client, product):
    """
    Test function to verify that a user without group permission cannot create a product.

    @param client: The Django test client object.
    @param product: The Product object to be created.
    @return: None
    """

    data = {
        "sku": product.sku,
        "name": product.name,
        "price": str(product.price),
        "brand": product.brand,
    }

    # Set the expected HTTP response code to 403 (FORBIDDEN)
    expected = status.HTTP_403_FORBIDDEN

    # Send a POST request to the 'products-list' endpoint with the product data
    response = client.post(reverse("products-list"), data=data)

    # Verify that the response status code matches the expected code
    assert response.status_code == expected


def test_create_product(user, product, mocker):
    """
    Test function to create a product using an authenticated user.

    @param user: The User object that will be authenticated.
    @param product: The Product object to be created.
    @param mocker: The mocker object to patch the ProductAdminOnly permission class.
    @return: None
    """
    # Create a test client and authenticate the user
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

    # Patch the ProductAdminOnly permission class to return True
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)

    # Send a POST request to the 'products-list' endpoint with the product data
    response = client.post(reverse("products-list"), data=data)
    received = [response.status_code, response.data]
    assert expected == received


def test_update_product(client, product, mocker):
    """
    Test function to update a product.

    @param client: The Django test client object.
    @param product: The Product object to be updated.
    @param mocker: The mocker object to patch the ProductAdminOnly permission class and notify_update_product method.
    @return: None
    """
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

    # Set the expected HTTP response code to 200 (OK) and the expected results
    expected = [status.HTTP_200_OK, expected_results]

    # Send a PATCH request to the 'products-detail' endpoint with the product data
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)
    notify_update_product = mocker.patch(
        "store.serializers.product_change_notification.delay"
    )
    response = client.patch(reverse("products-detail", args=(product.sku,)), data=data)
    received = [response.status_code, response.data]

    # Verify that the expected and received results match
    assert expected == received
    assert notify_update_product.called
    notify_update_product.assert_called_with(product.sku)


def test_delete_product(client, mocker):
    """
    Test function to delete a product.

    @param client: The Django test client object.
    @param mocker: The mocker object to patch the ProductAdminOnly permission class.
    @return: None
    """
    page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 4)
    prod_list = ProductFactory.create_batch(page_size)
    prod_to_delete = prod_list[1]
    mocker.patch("store.views.ProductAdminOnly.has_permission", return_value=True)

    # Send a DELETE request to the 'products-detail' endpoint with the product SKU
    response = client.delete(reverse("products-detail", args=(prod_to_delete.sku,)))

    # Verify that the response status code is 204 (NO CONTENT)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify that the number of products in the database is reduced by one
    objects = set(Product.objects.all())
    assert len(objects) == 3

    # Verify that the deleted product is no longer in the database
    prod_set = set(prod_list)
    prod_set.remove(prod_to_delete)
    assert prod_set == objects

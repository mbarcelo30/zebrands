from django.conf import settings

import pytest
from rest_framework.test import APIClient
from store.tests.factories import ProductFactory, ProductStatsFactory, UserFactory


@pytest.fixture()
def product():
    """
    Fixture to generate a Product instance for testing purposes.
    """
    return ProductFactory()


@pytest.fixture()
def product_stats():
    """
    Fixture to generate a ProductStats instance for testing purposes.
    """
    return ProductStatsFactory()


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    """
    Fixture to generate a User instance for testing purposes.
    """
    return UserFactory()


@pytest.fixture()
def client(user):
    """
    Fixture to generate an authenticated APIClient instance for testing purposes.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client

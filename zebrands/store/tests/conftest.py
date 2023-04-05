from django.conf import settings

import pytest
from rest_framework.test import APIClient
from store.tests.factories import ProductFactory, ProductStatsFactory, UserFactory


@pytest.fixture()
def product():
    return ProductFactory()


@pytest.fixture()
def product_stats():
    return ProductStatsFactory()


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture()
def client(user):
    # For users authenticated
    client = APIClient()
    client.force_authenticate(user=user)
    return client

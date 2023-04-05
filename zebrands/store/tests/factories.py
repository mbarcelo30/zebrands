from django.contrib.auth.models import User

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from store.models import Product, ProductStats


class ProductFactory(DjangoModelFactory):
    sku = Faker("bothify")
    name = Faker("color_name")
    price = Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    brand = Faker("company")

    class Meta:
        model = Product


class ProductStatsFactory(DjangoModelFactory):
    product = SubFactory(ProductFactory)
    view_count = Faker("pyint", min_value=1, max_value=100)

    class Meta:
        model = ProductStats


class UserFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = Faker("email")

    class Meta:
        model = User

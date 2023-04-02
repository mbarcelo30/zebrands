"""zebrands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from store.views import ProductViewSet
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"users", UserViewSet, basename="users")


urlpatterns = router.urls + [
    # DRF Authentication
    path("token/", obtain_auth_token, name="api_token_auth"),
    # Django admin
    path("admin/", admin.site.urls),
]

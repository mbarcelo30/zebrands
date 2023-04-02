from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from users.models import USER_ADMIN_GROUP
from users.serializers import UserSerializer


class UserViewSet(
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = "username"

    def perform_create(self, serializer):
        user = self.request.user
        get_object_or_404(Group, name=USER_ADMIN_GROUP)
        if user.groups.filter(name=USER_ADMIN_GROUP).exists():
            serializer.save()
        else:
            raise PermissionDenied("Don't have permission to create users")

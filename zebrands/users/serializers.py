from django.contrib.auth.models import Group, User

from rest_framework import serializers
from store.models import PRODUCT_ADMIN_GROUP
from users.models import USER_ADMIN_GROUP


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=128)
    username = serializers.CharField(required=True, max_length=128)
    first_name = serializers.CharField(required=False, max_length=128)
    last_name = serializers.CharField(required=False, max_length=128)

    class Meta:
        model = User
        read_only_fields = ["username"]
        fields = ["email", "password", "username", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        for group_name in (USER_ADMIN_GROUP, PRODUCT_ADMIN_GROUP):
            group = Group.objects.get(name=group_name)
            group.user_set.add(user)
        return user

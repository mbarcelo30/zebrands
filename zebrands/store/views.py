from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.models import PRODUCT_ADMIN_GROUP, Product
from store.serializers import ProductListSerializer, ProductSerializer
from store.tasks import product_update_counter


class ProductAdminOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.groups.filter(name=PRODUCT_ADMIN_GROUP).exists()


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = "sku"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ("retrieve", "list"):
            # Allow anonymous users to access the retrieve method
            permission_classes = [AllowAny]
        else:
            # Allow access only to authenticated users in the ProductAdmin group
            permission_classes = [IsAuthenticated, ProductAdminOnly]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_authenticated:
            product_update_counter.delay(instance.sku)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

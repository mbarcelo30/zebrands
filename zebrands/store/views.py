from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from store.models import PRODUCT_ADMIN_GROUP, Product
from store.serializers import ProductListSerializer, ProductSerializer
from store.tasks import product_update_counter


class ProductAdminOnly(BasePermission):
    """
    Permission class that allows access only to users in the 'ProductAdmin' group.
    """

    def has_permission(self, request, view):
        """
        Returns True if the user making the request is a member of the 'ProductAdmin' group.

        Args:
        - request: The HTTP request object.
        - view: The view object associated with the request.

        Returns:
        True if the user is a member of the 'ProductAdmin' group, False otherwise.
        """
        user = request.user
        return user.groups.filter(name=PRODUCT_ADMIN_GROUP).exists()


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = "sku"

    def get_serializer_class(self):
        """
        Returns the serializer class to use, depending on the requested action.

        If the action is 'list', returns the serializer class for the list of products.
        Otherwise, returns the serializer class for an individual product.
        """
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer

    def get_permissions(self):
        """
        Obtains a list of permissions that are required to perform the current action.

        For non-authenticated users, the 'list' and 'retrieve' actions are allowed.
        For authenticated users, only those in the 'ProductAdmin' group are allowed to access other actions.

        @return:
        A list of permission objects.
        """
        if self.action in ("retrieve", "list"):
            # Allow anonymous users to access the retrieve method
            permission_classes = [AllowAny]
        else:
            # Allow access only to authenticated users in the ProductAdmin group
            permission_classes = [IsAuthenticated, ProductAdminOnly]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single product instance.

        If the user is not authenticated, updates the product's view counter by scheduling a task using Celery.

        Returns:
        A response object containing the serialized product instance data.
        """
        instance = self.get_object()
        is_authenticated = request.user.is_authenticated
        if not is_authenticated:
            product_update_counter.delay(instance.sku)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

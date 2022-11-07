from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from testproject.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from users.auth import JWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin


class GenericProductView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class getallproduct(GenericProductView, ListModelMixin):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request,
                         *args,
                         **kwargs)


class productapi(GenericProductView,
                 CreateModelMixin,
                 UpdateModelMixin,
                 RetrieveModelMixin,
                 DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

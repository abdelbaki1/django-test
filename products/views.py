
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
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
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class getallproduct(GenericProductView,ListModelMixin):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    pagination_class = CustomPagination
class productapi(GenericProductView,
                CreateModelMixin,
                UpdateModelMixin,
                RetrieveModelMixin,
                DestroyModelMixin):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def post(self, request):
        return self.create(request, *args, **kwargs)
    def put(self, request, pk=None):
        return self.partial_update(request, *args, **kwargs)
    def delete(self, request, pk=None):
        return self.destroy(request, *args, **kwargs)
    lookup_field = "id"	
    lookup_url_kwarg = 'pk'

class FileUploadView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://localhost:8000/api' + url
        })

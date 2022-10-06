
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from admin.pagination import CustomPagination
from products.models import Product
from products.serializers import ProductSerializer
from users.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import UpdateAPIView

class ProductGenericAPIView(RetrieveUpdateDestroyAPIView,ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    lookup_field = id	
    lookup_url_kwarg = pk

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

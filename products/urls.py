from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import productapi, FileUploadView,getallproduct

urlpatterns = [
                  path('products/create', productapi.as_view()),
                  path('products', getallproduct.as_view()),
                  path('products/<int:pk>', productapi.as_view()),
                  path('upload', FileUploadView.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
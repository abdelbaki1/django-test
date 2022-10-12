from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import productapi, FileUploadView,getallproduct

urlpatterns = [
                  path('products', getallproduct.as_view()),
                  path('products/<str:pk>', productapi.as_view(),{'pk','pk'}),
                  path('upload', FileUploadView.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
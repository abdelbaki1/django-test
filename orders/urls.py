from django.urls import path

from .views import GetAllOrder,GetanOrder, ExportAPIView, ChartAPIView

urlpatterns = [
    path('orders', GetAllOrder.as_view()),#get all the orders
    path('orders/<int:pk>', GetanOrder.as_view()),
    path('export', ExportAPIView.as_view()),
    path('chart', ChartAPIView.as_view())]
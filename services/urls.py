from django.urls import path

from .views import ServiceDetailView, ServiceListCreateView, ServiceToggleView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('<int:pk>/<str:action>/', ServiceToggleView.as_view(), name='service-toggle'),
]

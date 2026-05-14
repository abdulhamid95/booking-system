from django.urls import path

from .views import PublicServiceListView, ServiceDetailView, ServiceListCreateView, ServiceToggleView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'),
    path('public/<int:business_id>/', PublicServiceListView.as_view(), name='service-public-list'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('<int:pk>/<str:action>/', ServiceToggleView.as_view(), name='service-toggle'),
]

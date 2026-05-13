from django.urls import path

from .views import StaffDetailView, StaffListCreateView, StaffToggleView

urlpatterns = [
    path('', StaffListCreateView.as_view(), name='staff-list-create'),
    path('<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('<int:pk>/<str:action>/', StaffToggleView.as_view(), name='staff-toggle'),
]

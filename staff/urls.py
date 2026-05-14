from django.urls import path

from .views import PublicStaffListView, StaffDetailView, StaffListCreateView, StaffToggleView

urlpatterns = [
    path('', StaffListCreateView.as_view(), name='staff-list-create'),
    path('public/<int:business_id>/<int:service_id>/', PublicStaffListView.as_view(), name='staff-public-list'),
    path('<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    path('<int:pk>/<str:action>/', StaffToggleView.as_view(), name='staff-toggle'),
]

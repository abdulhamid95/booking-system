from django.urls import path

from .views import PublicAvailableSlotsView, PublicBookingCreateView

urlpatterns = [
    path('', PublicBookingCreateView.as_view(), name='booking-create'),
    path('available-slots/', PublicAvailableSlotsView.as_view(), name='available-slots'),
]

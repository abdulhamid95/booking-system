from django.urls import path

from .views import BusinessProfileView

urlpatterns = [
    path('me/', BusinessProfileView.as_view(), name='business-profile'),
]
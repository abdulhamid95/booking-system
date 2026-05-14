from django.urls import path

from .views import BusinessRegisterView, LoginView, LogoutView, MeView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('register/business/', BusinessRegisterView.as_view(), name='auth-register-business'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', MeView.as_view(), name='auth-me'),
]

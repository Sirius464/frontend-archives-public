from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import login_view

urlpatterns = [
    path('auth/login/', login_view, name='api_login'),
]
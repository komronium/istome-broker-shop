from django.urls import path

from .views import *

urlpatterns = [
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('auth/register', RegisterAPIView.as_view(), name='register'),

    path('profile', ProfileAPIView.as_view(), name='profile')
]
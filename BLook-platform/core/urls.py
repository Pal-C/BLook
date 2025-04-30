from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.home, name='home'),
    path("auth/", views.auth_screen, name="auth_screen"),
]
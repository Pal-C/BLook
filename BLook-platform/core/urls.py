from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name='home'),
    path("auth/", views.auth_screen, name="auth_screen"),
    path('logout/', LogoutView.as_view(next_page='auth_screen'), name='custom_logout'),
    path("browse/", views.browse, name='browse'),
    path("upload/", views.upload_review, name='upload_review'),
    path("add/", views.add_review, name='add_review'), # reminder to add <int:book_id>/
]
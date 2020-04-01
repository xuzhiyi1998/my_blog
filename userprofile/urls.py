from django.urls import path
from django.urls.base import reverse_lazy
from django.contrib.auth.views import PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView
from .views import LoginView,LogoutView,RegisterView,UserDeleteView,EditUserView
urlpatterns=[
    path("login",LoginView.as_view(),name="login"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("register",RegisterView.as_view(),name="register"),
    path("delete/<int:pk>",UserDeleteView.as_view(),name="delete"),
    path("edit/<int:pk>",EditUserView.as_view(),name="edit"),
]
from django.urls import path
from .views import SignupView, SigninView, LogoutView, UserDetailView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", SigninView.as_view(), name="login"),
    path("me/", UserDetailView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

from django.urls import path
from .views import SignupView, SigninView, LogoutView, UserDetailView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("signin", SigninView.as_view(), name="signin"),
    path("me", UserDetailView.as_view(), name="me"),
    path("logout", LogoutView.as_view(), name="logout"),
]

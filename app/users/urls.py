from django.urls import path
from .views import SignupView, SigninView, LogoutView, UserDetailView

urlpatterns = [
    path("auth/signup", SignupView.as_view(), name="signup"),
    path("auth/signin", SigninView.as_view(), name="signin"),
    path("auth/me", UserDetailView.as_view(), name="me"),
    path("auth/logout", LogoutView.as_view(), name="logout"),
]

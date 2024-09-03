from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("auth/", include("users.urls")),
    #     path("comments/", include("comments.urls")),
    #     path("ws/comments/", include("app.comments.routing.websocket_urlpatterns")),
]

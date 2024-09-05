# urls.py
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from comments.routing import websocket_urlpatterns  # Импортируем напрямую
from comments.views import CommentViewSet

from .yasg import urlpatterns as doc_urls  # doc swagger


router = DefaultRouter()
router.register(r"", CommentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("captcha/", include("captcha.urls")),
    path("auth/", include("users.urls")),
    path("comments/", include(router.urls)),
    path(
        "ws/comments/", include(websocket_urlpatterns)
    ),  # Подключаем WebSocket маршруты
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += doc_urls

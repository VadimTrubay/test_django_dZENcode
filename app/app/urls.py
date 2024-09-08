# urls.py
from django.contrib import admin
from django.urls import path, include

from comments.routing import websocket_urlpatterns
from comments.urls import router


urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/", include("users.urls")),
    path("api/v1/", include(router.urls)),
    path("captcha/", include("captcha.urls")),
    path(
        "api/v1/api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
    path("ws/", include(websocket_urlpatterns)),
]

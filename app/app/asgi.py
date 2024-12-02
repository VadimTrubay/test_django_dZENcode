import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from comments.consumers import CommentConsumer
from comments.middleware import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(  # Ваш middleware для WebSocket
            URLRouter(
                [
                    path("ws/comments/", CommentConsumer.as_asgi()),  # Пример маршрута
                ]
            )
        ),
    }
)

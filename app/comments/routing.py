# routing.py
from django.urls import re_path
from .consumers import CommentConsumer

websocket_urlpatterns = [
    re_path(r"comments/$", CommentConsumer.as_asgi()),
]

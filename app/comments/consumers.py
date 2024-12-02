import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Comment
from .serializers import CommentSerializer


class CommentConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        # Получаем пользователя из scope
        user = self.scope.get("user")

        if user is None:
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            return

        data = json.loads(text_data)
        parent_id = data.get("parent_id")

        # Асинхронно получаем пользователя
        user = await self.get_user(user.id)

        # Создаем комментарий
        comment = await self.create_comment(user, data["message"], parent_id)

        # Сериализуем комментарий
        serialized_comment = await self.serialize_comment(comment)

        # Отправляем комментарий всем подписчикам
        await self.channel_layer.group_send(
            "comments", {"type": "comment_message", "message": serialized_comment}
        )

    @database_sync_to_async
    def serialize_comment(self, comment):
        return CommentSerializer(comment).data

    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()  # Используем кастомную модель пользователя
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_comment(self, user, message, parent_id):
        comment = Comment.objects.create(
            user=user,
            text=message,
            parent_id=parent_id if parent_id else None,
        )
        # Предзагружаем связанные ответы
        return Comment.objects.prefetch_related('replies').get(id=comment.id)

    async def comment_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

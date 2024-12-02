# consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Comment
from .serializers import CommentSerializer


class CommentConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        parent_id = data.get("parent_id")

        # Get the user from the scope
        user = self.scope["user"]

        # Use sync_to_async to perform the database query in a non-blocking way
        user = await self.get_user(user.id)

        # Create the comment
        comment = await self.create_comment(user, data["message"], parent_id)

        # Serialize and broadcast the comment
        serialized_comment = CommentSerializer(comment).data
        await self.channel_layer.group_send(
            "comments", {"type": "comment_message", "message": serialized_comment}
        )

    # Use sync_to_async to handle synchronous DB calls in an async context
    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()  # Ensure you're using the custom user model
        return User.objects.get(id=user_id)

    # Similarly for creating the comment
    @database_sync_to_async
    def create_comment(self, user, message, parent_id):
        return Comment.objects.create(
            user=user,
            text=message,
            parent_id=parent_id if parent_id else None,
        )

    async def comment_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

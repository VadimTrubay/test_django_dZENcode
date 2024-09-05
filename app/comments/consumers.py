# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comment
from .serializers import CommentSerializer


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("comments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        parent_id = data.get("parent_id")
        comment = Comment.objects.create(
            user=self.scope["user"],
            text=data["message"],
            parent_id=parent_id if parent_id else None,
        )
        serialized_comment = CommentSerializer(comment).data

        await self.channel_layer.group_send(
            "comments", {"type": "comment_message", "message": serialized_comment}
        )

    async def comment_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

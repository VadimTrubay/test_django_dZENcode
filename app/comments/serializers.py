from asgiref.sync import sync_to_async
from rest_framework import serializers
from comments.models import Comment
from users.serializers import CustomUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    async def get_replies(self, obj):
        # Асинхронно получаем связанные комментарии
        replies = await sync_to_async(lambda: list(obj.replies.all()))()
        return CommentSerializer(replies, many=True, context=self.context).data

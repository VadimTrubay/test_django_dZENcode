# serializers.py
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    # replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"
        # fields = ["id", "user", "text", "parent", "created_at"]

    # def get_replies(self, obj):
    #     if obj.replies.exists():
    #         return CommentSerializer(obj.replies.all(), many=True).data
    #     return []

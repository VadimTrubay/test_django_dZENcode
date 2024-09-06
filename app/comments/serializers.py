# serializers.py
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_replies(self, obj):
        # Limit to only top-level replies (no recursion for nested replies)
        max_depth = self.context.get("max_depth", 1)
        if max_depth > 0 and obj.replies.exists():
            # Reduce depth by 1 for nested replies
            return CommentSerializer(
                obj.replies.all(), many=True, context={"max_depth": max_depth - 1}
            ).data
        return []

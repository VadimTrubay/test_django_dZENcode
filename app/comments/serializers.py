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
        # Fetch and serialize all replies recursively, without limiting depth
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.all(),
                many=True,
                context=self.context,  # Pass context if necessary
            ).data
        return []

# view.py
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import (
    IsAuthenticated,
)


class CommentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 25


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        "created_at",
        "user__username",
        "user__email",
    ]
    ordering = ["created_at"]
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_create(self, serializer):
    #     # В случае создания комментария можно указать parent, если это ответ
    #     parent = self.request.data.get('parent', None)
    #     if parent:
    #         parent_comment = Comment.objects.get(id=parent)
    #         serializer.save(parent=parent_comment)
    #     else:
    #         serializer.save()

    # def perform_create(self, serializer):
    #     # Получаем родителя из данных запроса (если он был передан)
    #     parent_id = self.request.data.get('parent')
    #
    #     if parent_id:
    #         try:
    #             # Проверяем, существует ли комментарий с указанным ID родителя
    #             parent_comment = Comment.objects.get(id=parent_id)
    #             serializer.save(user=self.request.user, parent=parent_comment)
    #         except Comment.DoesNotExist:
    #             # Обработка случая, если родительский комментарий не найден
    #             raise serializers.ValidationError("Родительский комментарий не найден.")
    #     else:
    #         # Если родитель не указан, сохраняем комментарий как корневой
    #         serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        user_id = instance.user.id
        if user_id != request.user.id:
            return Response(
                {"error": "You cannot delete this comment"},
                status=status.HTTP_403_FORBIDDEN,
            )
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)

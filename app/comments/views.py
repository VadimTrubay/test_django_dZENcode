# view.py
from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)


class CommentPagination(PageNumberPagination):
    page_size = 25  # Количество объектов на страницу
    page_size_query_param = "page_size"  # Опционально: возможность изменения размера страницы через параметр запроса
    max_page_size = 25  # Максимальный размер страницы


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]  # Добавляем backend для сортировки
    ordering_fields = [
        "created_at",
        "user__username",
        "user__email",
    ]  # Указываем доступные для сортировки поля
    ordering = ["created_at"]  # Сортировка по умолчанию
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        user_id = instance.user.id
        if user_id != request.user.id:
            return Response({"error": "You cannot delete this comment"}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"id": instance_id}, status=status.HTTP_200_OK)


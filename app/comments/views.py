# view.py
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)


class CommentPagination(PageNumberPagination):
    page_size = 5  # Количество объектов на страницу
    page_size_query_param = "page_size"  # Опционально: возможность изменения размера страницы через параметр запроса
    max_page_size = 100  # Максимальный размер страницы


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

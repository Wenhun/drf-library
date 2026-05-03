from library.serializers import *
from rest_framework import viewsets, status
from library.models import Book
from rest_framework.serializers import ModelSerializer

from typing import Type


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author")
    serializer_class = BookDetailSerializer

    def get_serializer_class(self) -> Type[ModelSerializer]:
    """Return the appropriate serializer class based on the request."""

    if self.action == "list":
        return BookListSerializer

    if self.action == "retrieve":
        return BookDetailSerializer

    return super().get_serializer_class()

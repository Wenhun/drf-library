from library.serializers import *
from library.permissions import IsAdminOrIfAuthenticatedReadOnly
from rest_framework import viewsets, status
from library.models import Author, Book
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAdminUser

from typing import Type


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related("author")
    serializer_class = BookDetailSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        """Return the appropriate serializer class based on the request."""

        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        return super().get_serializer_class()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminUser,)

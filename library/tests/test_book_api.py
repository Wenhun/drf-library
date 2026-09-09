from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Author, Book
from library.serializers import AuthorSerializer, BookListSerializer
from library.tests.test_author_api import sample_author

BOOK_URL = reverse("library:books-list")


def sample_book(**params):
    defaults = {"title": "test", "cover": "SOFT"}
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BOOK_URL)
        # TODO: FIX TO 401 ERROR
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_movies(self):
        sample_book()
        sample_book()

        res = self.client.get(BOOK_URL)

        movies = Book.objects.order_by("id")
        serializer = BookListSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        payload = {"title": "test", "cover": "SOFT"}
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        author = sample_author()
        payload = {
            "title": "test",
            "cover": "soft",
        }
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(book, key))

    def test_create_book_with_authors(self):
        author_1 = sample_author()
        author_2 = sample_author()
        payload = {
            "title": "test",
            "author_ids": [author_1.pk, author_2.pk],
            "cover": "soft",
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(id=res.data["id"])
        authors = book.author.all()
        self.assertEqual(authors.count(), 2)
        self.assertIn(author_1, authors)
        self.assertIn(author_2, authors)

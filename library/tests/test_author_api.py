from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Author
from library.serializers import AuthorSerializer

AUTHOR_URL = reverse("library:authors-list")


def sample_author(**params):
    defaults = {
        "first_name": "test First",
        "last_name": "test Last",
        "middle_name": "test Middle",
    }
    defaults.update(params)

    return Author.objects.create(**defaults)


class AuthorPermissionsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_no_auth_forbidden(self):
        res = self.client.get(AUTHOR_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_admin_forbidden(self):
        self._assert_author_list_forbidden(is_staff=False)

    def test_admin_allowed(self):
        self._assert_author_list_status(status.HTTP_200_OK, is_staff=True)

    def _assert_author_list_forbidden(self, is_staff):
        self._assert_author_list_status(status.HTTP_403_FORBIDDEN, is_staff)

    def _assert_author_list_status(self, expected_status, is_staff):
        user = get_user_model().objects.create_user(
            "admin@admin.com", "test_password", is_staff=is_staff
        )
        self.client.force_authenticate(user)
        response = self.client.get(AUTHOR_URL)
        self.assertEqual(response.status_code, expected_status)


class AdminAuthorApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "test_password", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_list_authors(self):
        sample_author()
        sample_author()

        res = self.client.get(AUTHOR_URL)

        movies = Author.objects.order_by("id")
        serializer = AuthorSerializer(movies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_author(self):
        payload = {
            "first_name": "test First",
            "last_name": "test Last",
            "middle_name": "test Middle",
        }
        res = self.client.post(AUTHOR_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(author, key))

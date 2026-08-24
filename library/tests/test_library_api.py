from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

AUTHOR_URL = reverse("library:authors-list")


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

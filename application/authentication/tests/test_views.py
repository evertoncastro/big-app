import django

django.setup()
from django.db import transaction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from application.authentication.models import User


class RegisterViewTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse("rest_register")

    def test_registration(self):
        user_data = {
            "email": "test@example.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }
        response = self.client.post(self.register_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="test@example.com")
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
        self.assertEqual(
            response.data["user"],
            {
                "pk": user.pk,
                "email": "test@example.com",
                "first_name": "",
                "last_name": "",
            },
        )
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_registration_email_conflict(self):
        User.objects.create_user(email="user1@example.com", password=None)
        self.assertTrue(User.objects.filter(email="user1@example.com").exists())

        with transaction.atomic():
            user_data = {
                "username": "user1",
                "email": "user11@example.com",
                "password1": "TestPassword123",
                "password2": "TestPassword123",
            }
            response = self.client.post(self.register_url, user_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):

    def setUp(self):
        self.login_url = reverse("rest_login")
        self.user = User.objects.create_user(
            email="user1@example.com", password="TestPassword123"
        )

    def test_login(self):
        user_data = {"email": self.user.email, "password": "TestPassword123"}

        response = self.client.post(self.login_url, user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
        self.assertLessEqual(
            {"email": self.user.email, "pk": self.user.id}.items(),
            response.data["user"].items(),
        )

import django

django.setup()
from django.test import TestCase

from application.authentication.models import User


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password=None)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_staff=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )

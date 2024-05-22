import django
django.setup()
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from application.authentication.models import User
from django.db import transaction


class RegisterViewTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('rest_register')

    def test_registration(self):
        user_data = {
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


    def test_registration_email_conflict(self):
        User.objects.create_user(email="user1@example.com", password=None)
        self.assertTrue(User.objects.filter(email='user1@example.com').exists())

        with transaction.atomic():
            user_data = {
                'username': 'user1',
                'email': 'user11@example.com',
                'password1': 'TestPassword123',
                'password2': 'TestPassword123'
            }
            response = self.client.post(self.register_url, user_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

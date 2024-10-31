# tests/test_token_auth.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenAuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Apassword69")
        self.token_url = reverse('token_obtain_pair')
        self.protected_url = reverse('goal-creation') 

    def test_obtain_token_success(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'Apassword69'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data['access']

    def test_access_protected_endpoint_with_token(self):
        token_response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'Apassword69'})
        access_token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.protected_url, {'user_input': 'I want to complete a goal'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_access_protected_endpoint_without_token(self):
        response = self.client.post(self.protected_url, {'user_input': 'I want to complete a goal'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

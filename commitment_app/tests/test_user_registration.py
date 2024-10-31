from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.url = reverse('user-register')

    def test_user_registration_success(self):
        data = {
            'username': 'testuser',
            'password': 'Apassword69',
            'password_confirm': 'Apassword69',  # Added this line
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')

        # Debugging output if registration fails
        if response.status_code != status.HTTP_201_CREATED:
            print("Registration failed:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_failure_missing_fields(self):
        data = {
            'username': '',
            'password': '',
            'password_confirm': '', 
            'email': ''
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

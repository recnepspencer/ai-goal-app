# tests/test_goal_creation.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class GoalCreationTests(APITestCase):

    def setUp(self):
        self.url = reverse('goal-creation')
        self.username = 'testuser'
        self.password = 'Apassword69'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def authenticate(self):
        # Log in and get the token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    @patch('commitment_app.services.openai_set_goal_service.OpenAISetGoalService.generate_goal')
    def test_goal_creation_success(self, mock_generate_goal):
        self.authenticate()
        # Mock a timezone-aware deadline
        deadline = timezone.make_aware(timezone.datetime(2024, 12, 31, 23, 59, 59))
        mock_generate_goal.return_value = {
            'name': 'run a mile',
            'description': 'run one mile every day',
            'deadline': deadline.strftime("%Y-%m-%d %H:%M:%S"),
            'priority': 'high'
        }
        data = {'user_input': 'I want to run a mile every day.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_goal_creation_failure_unauthenticated(self):
        data = {'user_input': 'I want to run a mile every day.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('commitment_app.services.openai_set_goal_service.OpenAISetGoalService.generate_goal')
    def test_goal_creation_failure_invalid_input(self, mock_generate_goal):
        self.authenticate()
        mock_generate_goal.return_value = None
        data = {'user_input': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

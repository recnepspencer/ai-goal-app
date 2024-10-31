# tests/test_goal_completion.py

from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model
from commitment_app.models.goal_model import Goal
from commitment_app.models.user_goal_model import UserGoal
from django.utils import timezone

User = get_user_model()

class GoalCompletionTests(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'Apassword69'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # Make deadline timezone-aware
        deadline = timezone.make_aware(timezone.datetime(2024, 12, 31, 23, 59, 59))

        self.goal = Goal.objects.create(
            name='run a mile',
            description='run one mile every day',
            deadline=deadline,
            priority='high'
        )
        self.user_goal = UserGoal.objects.create(user=self.user, goal=self.goal, progress=0)
        self.url = reverse('goal-completion', args=[self.goal.id])

    def authenticate(self):
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    @patch('commitment_app.services.openai_complete_goal_service.OpenAICompleteGoalService.validate_goal_completion')
    def test_goal_completion_success(self, mock_validate_goal_completion):
        self.authenticate()
        mock_validate_goal_completion.return_value = {'is_completed': True, 'message': 'Well done!'}
        data = {'user_explanation': 'I ran my mile today.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_completed'])

    @patch('commitment_app.services.openai_complete_goal_service.OpenAICompleteGoalService.validate_goal_completion')
    def test_goal_completion_needs_more_info(self, mock_validate_goal_completion):
        self.authenticate()
        mock_validate_goal_completion.return_value = {'is_completed': False, 'message': 'Can you provide more details?'}
        data = {'user_explanation': 'I ran.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_completed'])
        self.assertEqual(response.data['message'], 'Can you provide more details?')

    def test_goal_completion_failure_unauthenticated(self):
        data = {'user_explanation': 'I ran my mile today.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_goal_completion_failure_goal_not_found(self):
        self.authenticate()
        invalid_url = reverse('goal-completion', args=[9999])  # Assuming this ID doesn't exist
        data = {'user_explanation': 'I ran my mile today.'}
        response = self.client.post(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

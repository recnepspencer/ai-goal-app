from django.test import TestCase
from unittest.mock import patch
from commitment_app.services.openai_complete_goal_service import OpenAICompleteGoalService

class OpenAICompleteGoalServiceTests(TestCase):

    @patch('commitment_app.services.openai_complete_goal_service.client.beta.chat.completions.parse')
    def test_validate_goal_completion_success(self, mock_parse):
        mock_response = type('MockResponse', (object,), {
            'choices': [type('Choice', (object,), {'message': type('Message', (object,), {'parsed': type('Parsed', (object,), {
                'model_dump': lambda: {
                    'is_completed': True,
                    'message': 'Great job completing your goal!'
                }
            })})})]
        })
        mock_parse.return_value = mock_response
        goal_data = {
            'name': 'run a mile',
            'description': 'run one mile every day',
            'deadline': '2024-12-31 23:59:59',
            'priority': 'high'
        }
        result = OpenAICompleteGoalService.validate_goal_completion(goal_data, 'I ran my mile today.')
        self.assertIsNotNone(result)
        self.assertTrue(result['is_completed'])

    @patch('commitment_app.services.openai_complete_goal_service.client.beta.chat.completions.parse')
    def test_validate_goal_completion_failure(self, mock_parse):
        mock_parse.side_effect = Exception('API Error')
        goal_data = {
            'name': 'run a mile',
            'description': 'run one mile every day',
            'deadline': '2024-12-31 23:59:59',
            'priority': 'high'
        }
        result = OpenAICompleteGoalService.validate_goal_completion(goal_data, 'I ran my mile today.')
        self.assertIsNone(result)

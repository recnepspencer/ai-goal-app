from django.test import TestCase
from unittest.mock import patch
from commitment_app.services.openai_set_goal_service import OpenAISetGoalService

class OpenAISetGoalServiceTests(TestCase):

    @patch('commitment_app.services.openai_set_goal_service.client.beta.chat.completions.parse')
    def test_generate_goal_success(self, mock_parse):
        mock_response = type('MockResponse', (object,), {
            'choices': [type('Choice', (object,), {'message': type('Message', (object,), {'parsed': type('Parsed', (object,), {
                'model_dump': lambda: {
                    'name': 'run a mile',
                    'description': 'run one mile every day',
                    'deadline': '2024-12-31 23:59:59',
                    'priority': 'high'
                }
            })})})]
        })
        mock_parse.return_value = mock_response
        result = OpenAISetGoalService.generate_goal('I want to run a mile every day.')
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'run a mile')

    @patch('commitment_app.services.openai_set_goal_service.client.beta.chat.completions.parse')
    def test_generate_goal_failure(self, mock_parse):
        mock_parse.side_effect = Exception('API Error')
        result = OpenAISetGoalService.generate_goal('I want to run a mile every day.')
        self.assertIsNone(result)

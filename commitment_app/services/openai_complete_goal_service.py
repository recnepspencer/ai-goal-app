# services/openai_complete_goal_service.py

from pydantic import BaseModel
from openai import OpenAI
from django.conf import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class GoalCompletionResponse(BaseModel):
    is_completed: bool
    message: str

class OpenAICompleteGoalService:
    @staticmethod
    def validate_goal_completion(goal_data, user_explanation):
        """
        Validates if the goal is completed based on user's explanation.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that helps verify if a user has completed their goal. "
                    "The goal details are provided along with the user's explanation. "
                    "Be slightly skeptical and ask clarifying questions if necessary. "
                    "If the user failed to complete the goal or provides insufficient information, "
                    "refuse to mark the goal as complete."
                ),
            },
            {
                "role": "assistant",
                "content": f"Goal Details:\nName: {goal_data['name']}\nDescription: {goal_data.get('description', 'N/A')}\nDeadline: {goal_data['deadline']}\nPriority: {goal_data['priority']}",
            },
            {"role": "user", "content": user_explanation},
        ]

        try:
            # Use the `parse` method with the Pydantic model
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=messages,
                response_format=GoalCompletionResponse,
            )

            # Extract structured data from the response
            result = completion.choices[0].message.parsed
            return result.model_dump()  # Convert to a dictionary for serialization

        except Exception as e:
            print(f"OpenAI API error: {e}")  # Log the exception
            return None

from pydantic import BaseModel
from openai import OpenAI
from django.conf import settings
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Define the structured response model with Pydantic
class GoalResponse(BaseModel):
    name: str
    description: str
    deadline: str
    priority: str

class OpenAISetGoalService:
    @staticmethod
    def generate_goal(user_input):
        """
        Sends user input to OpenAI API and returns structured goal data.
        """
        # Get the current date and time in the required format
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the current date to the user's input for context
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that helps users define their goals. "
                    "Extract the goal information from the user's input. If the user does not provide a priority or name, make one up. "
                    "Make sure everything is in lower case. Format the date in YYY-MM-DD HH:MM:SS. Today's date is: " + current_date
                ),
            },
            {"role": "user", "content": user_input},
        ]

        try:
            # Use the `parse` method with the Pydantic model
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini-2024-07-18",
                messages=messages,
                response_format=GoalResponse,  # Specify the Pydantic model directly
            )

            # Extract structured data from the response
            goal_data = completion.choices[0].message.parsed
            return goal_data.model_dump()  # Convert to a dictionary for serialization

        except Exception as e:
            print(f"OpenAI API error: {e}")  # Log the exception
            return None

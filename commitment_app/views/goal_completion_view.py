# views/goal_completion_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..services.openai_complete_goal_service import OpenAICompleteGoalService
from ..models.user_goal_model import UserGoal

class GoalCompletionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, goal_id):
        user_explanation = request.data.get('user_explanation')
        if not user_explanation:
            return Response({"error": "User explanation is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the UserGoal instance for the current user and goal_id
        try:
            user_goal = UserGoal.objects.get(goal_id=goal_id, user=request.user)
        except UserGoal.DoesNotExist:
            return Response({"error": "Goal not found or not assigned to this user."}, status=status.HTTP_404_NOT_FOUND)

        # Access the goal details via the UserGoal instance
        goal = user_goal.goal

        # Prepare goal data
        goal_data = {
            'name': goal.name,
            'description': goal.description,
            'deadline': goal.deadline.strftime("%Y-%m-%d %H:%M:%S"),
            'priority': goal.priority,
        }

        # Validate goal completion using OpenAI
        validation_result = OpenAICompleteGoalService.validate_goal_completion(goal_data, user_explanation)
        if not validation_result:
            return Response({"error": "Failed to validate goal completion."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Handle the assistant's response
        if validation_result['is_completed']:
            # Mark the goal as completed in the UserGoal instance
            user_goal.progress = 100  # Assuming 100% means completion
            user_goal.save()
            return Response({"message": validation_result['message'], "is_completed": True}, status=status.HTTP_200_OK)
        else:
            # Do not mark as completed, return assistant's message
            return Response({"message": validation_result['message'], "is_completed": False}, status=status.HTTP_200_OK)

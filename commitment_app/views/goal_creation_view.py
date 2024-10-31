from ..services.openai_set_goal_service import OpenAISetGoalService
from ..serializers.goal_serializer import GoalSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from ..models.user_goal_model import UserGoal 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class GoalCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_input = request.data.get('user_input')
        if not user_input:
            return Response({"error": "User input is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Use OpenAISetGoalService to generate goal data
        goal_data = OpenAISetGoalService.generate_goal(user_input)
        if not goal_data:
            return Response({"error": "Failed to generate goal data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Normalize priority to lowercase
        goal_data['priority'] = goal_data.get('priority', 'medium').lower()


        try:
            goal_data['deadline'] = datetime.strptime(goal_data['deadline'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return Response({"error": "Deadline must be in YYYY-MM-DD HH:MM:SS format."}, status=status.HTTP_400_BAD_REQUEST)


        serializer = GoalSerializer(data=goal_data)
        if serializer.is_valid():
            goal = serializer.save() 

            UserGoal.objects.create(user=request.user, goal=goal, progress=0)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

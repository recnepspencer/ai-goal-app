from rest_framework import serializers
from ..models.goal_model import Goal

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name', 'description', 'deadline', 'is_completed', 'priority', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_completed', 'created_at', 'updated_at']

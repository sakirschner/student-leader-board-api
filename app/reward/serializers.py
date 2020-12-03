from django.contrib.auth import get_user_model

from rest_framework import serializers
from core.models import Reward


class RewardSerializer(serializers.ModelSerializer):
    """Serializer for reward objects"""

    class Meta:
        model = Reward
        fields = ('id', 'reward', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


# class StudentAchievementSerializer(serializers.ModelSerializer):
#     """Serializer for studentachievement objects"""
#     student = serializers.PrimaryKeyRelatedField(
#         many=False,
#         queryset=get_user_model().objects.all()
#     )
#     achievement = serializers.PrimaryKeyRelatedField(
#         many=False,
#         queryset=Achievement.objects.all()
#     )

#     class Meta:
#         model = StudentAchievement
#         fields = ('id', 'student', 'achievement', 'notes', 'created_at', 'updated_at')
#         read_only_fields = ('id', 'created_at', 'updated_at')
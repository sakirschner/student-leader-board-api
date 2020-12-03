from django.contrib.auth import get_user_model

from rest_framework import serializers
from core.models import Reward, StudentReward


class RewardSerializer(serializers.ModelSerializer):
    """Serializer for reward objects"""

    class Meta:
        model = Reward
        fields = ('id', 'reward', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class StudentRewardSerializer(serializers.ModelSerializer):
    """Serializer for studentreward objects"""
    student = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=get_user_model().objects.all()
    )
    reward = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Reward.objects.all()
    )

    class Meta:
        model = StudentReward
        fields = ('id', 'student', 'reward', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
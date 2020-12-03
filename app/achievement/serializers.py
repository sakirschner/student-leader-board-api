from rest_framework import serializers
from core.models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievement objects"""

    class Meta:
        model = Achievement
        fields = ('id', 'achievement', 'points', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


# class AchievementDetailsSerializer(serializers.ModelSerializer):
#     """Serialize acheivement objects"""

    # class Meta:
    #     model = Achievement
    #     fields = ('id', 'achievement', 'points', 'created_at', 'updated_at')
    #     read_only_fields = ('id', 'created_at', 'updated_at')
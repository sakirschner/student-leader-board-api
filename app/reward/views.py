from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Reward, StudentReward
from reward import serializers


class RewardViewSet(viewsets.GenericViewSet,
                         viewsets.ViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Manage Rewards in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reward.objects.all()
    serializer_class = serializers.RewardSerializer

    def get_queryset(self):
        """Return all objects"""
        return self.queryset

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class GetRewardByIdView(generics.RetrieveUpdateDestroyAPIView):
    """Manage single reward from the database by id"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RewardSerializer

    def get_object(self, **kwargs):
        """Return object for user"""
        return Reward.objects.get(id=self.kwargs['pk'])


class StudentRewardViewSet(viewsets.GenericViewSet,
                         viewsets.ViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Manage Rewards in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = StudentReward.objects.all()
    serializer_class = serializers.StudentRewardSerializer

    def get_queryset(self):
        """Return all objects"""
        return self.queryset

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class GetStudentRewardByIdView(generics.RetrieveUpdateDestroyAPIView):
    """Lists single studentreward from the database by id"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.StudentRewardSerializer

    def get_object(self, **kwargs):
        """Return object for user"""
        return StudentReward.objects.get(id=self.kwargs['pk'])
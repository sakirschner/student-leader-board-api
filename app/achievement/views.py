from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from core.models import Achievement
from achievement import serializers


class AchievementViewSet(viewsets.GenericViewSet,
                         viewsets.ViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """Manage Achievements in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Achievement.objects.all()
    serializer_class = serializers.AchievementSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class GetAchievementByIdView(generics.RetrieveUpdateDestroyAPIView):
    """Lists single achievement from the database by id"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AchievementSerializer

    def get_object(self, **kwargs):
        """Return object for user"""
        return Achievement.objects.get(id=self.kwargs['pk'])

    # def retrieve(self, request, pk=None):
    #     """Return appropriate serializer class"""
    #     achievement = get_object_or_404(self.queryset, pk=pk)
    #     serializer = serializers.AchievementSerializer()
    #     print(serializer.data)
    #     return Response(serializer.data)
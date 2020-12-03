from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Achievement

from achievement.serializers import AchievementSerializer


ACHIEVEMENT_URL = reverse('achievement:achievement-list')


def sample_achievement(achievement='Had camera on for a full day'):
    """Create and return a sample achievement"""
    return Achievement.objects.create(achievement=achievement)

def detail_url(achievement_id):
    """Return acheviement detail URL"""
    return reverse('achievement:achievement', args=[achievement_id])


class PublicAchievementAPITests(TestCase):
    """Test the publically available achievement API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving Achievements"""
        res = self.client.get(ACHIEVEMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAchievementAPITests(TestCase):
    """Test the private achievement API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'scott@gmail.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_achievement_list(self):
        """Test retrieving a list of achievements"""
        Achievement.objects.create(achievement='Had camera on')
        Achievement.objects.create(achievement='Attended class')

        res = self.client.get(ACHIEVEMENT_URL)
        achievements = Achievement.objects.all().order_by('-achievement')
        serializer = AchievementSerializer(achievements, many=True)  
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_achievement_detail(self):
        """Testing viewing a single achievement"""
        achievement = sample_achievement()

        url = detail_url(achievement.id)
        res = self.client.get(url)
        serializer = AchievementSerializer(achievement)

        self.assertEqual(res.data, serializer.data)
    
        

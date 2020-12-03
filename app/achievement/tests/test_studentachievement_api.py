from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import StudentAchievement, Achievement

from achievement.serializers import StudentAchievementSerializer


STUDENTACHIEVEMENT_URL = reverse('achievement:studentachievement-list')


def sample_achievement(achievement='Had camera on for a full day'):
    """Create and return a sample achievement"""
    return Achievement.objects.create(achievement=achievement)

def sample_studentachievement(user, **params):
    """Create and return a sample studentachievement"""
    defaults = {
        'student': user,
        'achievement': sample_achievement(),
        'notes': 'sample test',
    }
    defaults.update(params)

    return StudentAchievement.objects.create(**defaults)

def detail_url(studentachievement_id):
    """Return studentacheviement detail URL"""
    return reverse('achievement:studentachievement', args=[studentachievement_id])


class PublicStudentAchievementAPITests(TestCase):
    """Test the publically available stedentachievement API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(STUDENTACHIEVEMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentAchievementAPITests(TestCase):
    """Test the private studentachievement API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'scott@gmail.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_studentachievement_list(self):
        """Test retrieving a list of student achievements"""
        sample_studentachievement(user=self.user)
        sample_studentachievement(user=self.user)

        res = self.client.get(STUDENTACHIEVEMENT_URL)

        studentachievements = StudentAchievement.objects.all()
        serializer = StudentAchievementSerializer(studentachievements, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_studentachievement_detail(self):
        """Testing viewing a single studentachievement"""
        studentachievement = sample_studentachievement(user=self.user)

        url = detail_url(studentachievement.id)
        res = self.client.get(url)
        serializer = StudentAchievementSerializer(studentachievement)

        self.assertEqual(res.data, serializer.data)
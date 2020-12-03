from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Reward

from reward.serializers import RewardSerializer


REWARD_URL = reverse('reward:reward-list')

def sample_reward(reward='fake trophy'):
    """Create and return a sample reward"""
    return Reward.objects.create(reward=reward)

def detail_url(reward_id):
    """Return acheviement detail URL"""
    return reverse('reward:reward', args=[reward_id])


class PublicRewardAPITests(TestCase):
    """Test the publically available reward API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving rewards"""
        res = self.client.get(REWARD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRewardAPITests(TestCase):
    """Test the private reward API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'scott@gmail.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reward_list(self):
        """Test retrieving a list of rewards"""
        Reward.objects.create(reward='Test reward 1')
        Reward.objects.create(reward='Test reward 2')

        res = self.client.get(REWARD_URL)
        rewards = Reward.objects.all()
        serializer = RewardSerializer(rewards, many=True) 
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_reward_detail(self):
        """Testing viewing a single reward"""
        reward = sample_reward()

        url = detail_url(reward.id)
        res = self.client.get(url)
        serializer = RewardSerializer(reward)

        self.assertEqual(res.data, serializer.data)
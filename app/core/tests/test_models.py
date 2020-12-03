from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from core.models import Achievement


def sample_user(email='scott@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)

def sample_achievement(achievement='Had camera on for a full day'):
    """Create and return a sample achievement"""
    return Achievement.objects.create(achievement=achievement)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'scottakirschner@gmail.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'scottakirschner@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'scottakirschner@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    @patch('uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct loaction"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/user/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_achievement_str(self):
        """Test the achievement string representation"""
        achievement = models.Achievement.objects.create(
            achievement='Had computer on',
            points=3
        )
        self.assertEqual(str(achievement), achievement.achievement)

    def test_studentachievement_str(self):
        """Test the studentachievement string representation"""
        studentachievement = models.StudentAchievement.objects.create(
            student=sample_user(),
            achievement=sample_achievement(),
            notes='sample test'
        )

        self.assertEqual(str(studentachievement), studentachievement.achievement.achievement)

    def test_reward_str(self):
        """Test the reward string representation"""
        reward = models.Reward.objects.create(
            reward='Test Reward',
            description='Test Description'
        )
        self.assertEqual(str(reward), reward.reward)
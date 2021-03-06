import tempfile
import os

from PIL import Image 

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params): 
    return get_user_model().objects.create_user(**params)

def image_upload_url(user_id):
    """Return URL for user image upload"""
    return reverse('user:user-upload-image', args=[user_id])

# def detail_url(recipe_id):
#     """Return recipe deatail URL"""
#     return reverse('recipe:recipe-detail', args=[recipe_id])

class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'testpass123',
            'first_name': 'scott',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=res.data['id'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'testpass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'pw',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='scott@gmail.com', password='testpass')
        payload = {
            'email': 'scott@gmail.com',
            'password': 'wrong',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that the token is not created if the user doesn't exist"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {
                'email': 'scott@gmail.com',
                'password': '',
            })
        
        self.assertNotIn('token', res.data) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='scottakirschner@gmail.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
       """Test retrieving profile for logged in user"""
       res = self.client.get(ME_URL)

       self.assertEqual(res.status_code, status.HTTP_200_OK)
       self.assertEqual(res.data['id'], self.user.id)
    
    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'email': 'scott@gmail.com',
            'password': 'testpass',
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))        
        self.assertEqual(res.status_code, status.HTTP_200_OK)

class UserImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()       
        self.user = get_user_model().objects.create_user(
            'scott@gmail.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.user.image.delete()

    def test_upload_image_to_user(self):
        """Test uploading an image to a user"""
        url = image_upload_url(self.user.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10,10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart') 

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.user.image.path))
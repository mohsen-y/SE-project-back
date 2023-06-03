from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserCreateAPIviewTest(APITestCase):
	def setUp(self):
		self.client = APIClient()

	def test_create_user(self):
		url = "/users/sign-up/"
		data = {
			"email": "email@email.com",
    		"phone": 9123456789,
    		"password": "ََAa123456*",
    		"password_confirm": "ََAa123456*",
		}
		response = self.client.post(url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

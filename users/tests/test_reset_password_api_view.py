from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ResetPasswordAPIViewTest(APITestCase):
	def setUp(self):
		self.client = APIClient()

	def test_reset_password(self):
		url = "/users/reset-password/"
		data = {
			"email": "email@email.com",
			"password": "ََAa123456*",
			"password_confirm": "ََAa123456*",
			"code": "123456",
		}
		response = self.client.put(url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		
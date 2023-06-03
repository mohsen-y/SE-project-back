from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class sendOTPAPIViewTest(APITestCase):
	def setUp(self):
		self.client = APIClient()

	def test_send_otp(self):
		url = "/users/send-otp/"
		data = {
			"email": "email@email.com",
		}
		response = self.client.put(url, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
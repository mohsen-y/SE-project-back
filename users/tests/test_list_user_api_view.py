from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ListUserAPIViewTest(APITestCase):
	def setUp(self):
		self.client = APIClient()

	def test_list_user(self):
		url = "/users/"
		response = self.client.get(url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
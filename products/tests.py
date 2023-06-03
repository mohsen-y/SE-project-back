from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product
from rest_framework.test import APIClient
from users.models import User
from products.models import Product
from django.views.decorators.csrf import csrf_protect



class ProductTests(APITestCase):
    base_url = 'http://localhost:8000/products/'
    test_user_pass = "123456"
    test_user_email = "shayan@gmail.com"

    def setUp(self):
        User.objects.create(role = "admin" , email=self.test_user_email, password=self.test_user_pass)
        Product.objects.create(
            title='this is a test',
            brand= 'Gucci',
            type= 'running',
            price= '10',
            details= {},
            description= 'description for test',
            gender= 'both',
            images= {},
        )
        return super(ProductTests, self).setUp()

    def authenticate(self):
        user = User.objects.get(email=self.test_user_email)
        self.client.login(username=self.test_user_email, password=self.test_user_pass)
        self.client.force_authenticate(user=user)
    
    def test_create_product(self):
        """
        Ensure we can create a new product object.
        """
        url = reverse('create') 
        data = {
            'title': 'this is a test',
            'brand': 'Gucci',
            'type': 'running',
            'price': '10',
            'details': {},
            'description': 'description for test',
            'gender': 'both',
            'images': {},
            }
            
        self.authenticate()
        response = self.client.post(self.base_url + 'create/', data, format='json')
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
    

    def test_list_product(self):
       
        url = reverse('create') 
        
        response = self.client.get(self.base_url + 'list/')
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_RetrieveAPIView_product(self):
        
        productT = Product.objects.get(gender='both')
        pk= productT.id
        response = self.client.get(self.base_url + "{}/".format(pk)) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_UpdateAPIView_product(self):
        
        productT = Product.objects.get(gender='both')
        pk= productT.id
        self.authenticate()
        response = self.client.get(self.base_url + "{}/".format(pk) + "update/") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_DestroyAPIView_product(self):
        
        productT = Product.objects.get(gender='both')
        pk= productT.id
        self.authenticate()
        response = self.client.get(self.base_url + "{}/".format(pk) + "delete/") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_CommentCreate_product(self):
        
        productT = Product.objects.get(gender='both')
        pk= productT.id
        response = self.client.get(self.base_url + "{}/".format(pk) + "comments/create/") 
        csrf_token = response.cookies['csrftoken'].value
        comment_data = {
            'message': 'This is a test comment',
            'product': pk
        }
        response = self.client.post(self.base_url + "{}/".format(pk) + "comments/create/", data = comment_data) 

        self.authenticate()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


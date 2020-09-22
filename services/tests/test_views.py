from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import CustomUser
from services.models import Item

class ItemTest(APITestCase):
    def setUp(self):

        '''simple test database setup'''
        self.file = SimpleUploadedFile('joke.doc', b'I have no idea what I am writing:)', content_type='text/plain')
        self.client = APIClient()
        self.user = self.client.post('/register/', data={
            'first_name': 'test',
            'last_name': 'user',
            'password1': 'passworddd1234',
            'password2': 'passworddd1234',
            'email': 'test@example.com',
            'username': 'myuser1'
        })

        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'test@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)
        self.user2 = get_user_model().objects.create_admin(
            email='admin@example.com',
            password='passworddd1234',
            first_name='admin',
            last_name='user2',
            username='admin'
        )
        # self.item1 = Item.objects.create(
        #     name='item1',
        #     file=self.file,
        #     owner=self.owner,
        #     is_accessible=True
        # )
    
    def tearDown(self):
        return super().tearDown()
    
    def test_user_can_upload_file(self):

        '''Test for user upload'''
        self.item2 ={
            'name':'item2',
            'file':self.file,
            'owner':self.user,
            'is_accessible':False
        }
        response = self.client.post('/services/upload/', data=self.item2)
        res = Item.objects.all().count()
        self.assertEqual(res, 1)
    
    def test_user_can_edit_uploaded_file(self):

        '''Test for file edit'''
        file = SimpleUploadedFile('play.pdf', b'file_content', content_type='application/pdf')
        self.item2 ={
            'name': 'changed file',
            'file': self.file,
            'owner':  self.user,
            'is_accessible': False
        }
        response = self.client.put('/services/upload/1/', data=self.item2)
        self.assertEqual(response.data['name'], 'changed file')
    
    def test_user_can_delete_file(self):

        '''Test for file delete'''
        response = self.client.delete('/services/upload/1/')

        check = Item.objects.all()
        self.assertEqual(check.count(), 0)
    
    def test_admin_can_get_all_user_files(self):

        '''Test add can retrieve all files uploaded by users'''
        self.response = self.client.post(reverse('rest_login'), data={
            'email': 'admin@example.com',
            'password': 'passworddd1234',
        })
        self.token = self.response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ self.token)
        response = self.client.get('/services/upload/')

        self.assertEqual(response.data.count(), 1)
    
    def test_anyone_can_download_accessible_files(self):

        '''Test files flagged `is_accessible` true can be downloaded'''
        response = self.client.get('/services/download/1/')

        self.assertEqual(response.status, status.HTTP_200_OK)

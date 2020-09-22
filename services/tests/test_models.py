from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import CustomUser
from services.models import Item

class ItemTest(TestCase):
    def setUp(self):

        '''simple test database setup'''
        self.file = SimpleUploadedFile('joke.doc', b'I have no idea what I am writing:)', content_type='text/plain')
        self.owner = CustomUser.objects.create_user(
            'testuser@gmail.com',
            'myPasswordIsAPassword',
            first_name='tester',
            last_name='use',
            username='baby test'
        )
        self.item1 = Item.objects.create(
            name='item1',
            file=self.file,
            owner=self.owner,
            is_accessible=True
        )
    
    def tearDown(self):
        return super().tearDown()
    
    def test_user_can_upload_file(self):

        '''Test for user upload'''
        self.item2 = Item.objects.create(
            name='item2',
            file=self.file,
            owner=self.owner,
            is_accessible=False
        )
        res = Item.objects.all().count()
        self.assertEqual(res, 2)
    
    def test_user_can_edit_uploaded_file(self):

        '''Test for file edit'''
        my_file = Item.objects.get(id=1)
        my_file.name = 'changed file'
        my_file.file = SimpleUploadedFile('play.pdf', b'file_content', content_type='application/pdf')
        my_file.save()
        self.assertEqual(my_file.name, 'changed file')
    
    def test_user_can_delete_file(self):

        '''Test for file delete'''
        my_file = Item.objects.get(id=2)
        my_file.delete()
        check = Item.objects.all()
        self.assertEqual(check.count(), 1)

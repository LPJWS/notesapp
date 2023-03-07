from django.test import TestCase
from .models import *
import random
import string

class AuthTestCase(TestCase):
    def setUp(self):
        self.TEST_USER = {"username": "testuser", "password": "testpassword"}
        self.INVALID_USER = {"username": "testuser", "password": "corrupted"}

    def test_signup(self):
        response = self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        self.assertEqual(response.status_code, 201)

    def test_duplicate_signup(self):
        self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        response = self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        self.assertEqual(response.status_code, 400)

    def test_duplicate_signin_valid(self):
        self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        response = self.client.post('/api/v1/auth/signin/', data=self.TEST_USER)
        self.assertEqual(response.status_code, 200)

    def test_duplicate_signin_valid(self):
        self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        response = self.client.post('/api/v1/auth/signin/', data=self.INVALID_USER)
        self.assertEqual(response.status_code, 400)

    def test_get_me(self):
        response = self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        token = response.json()["token"]
        header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        response = self.client.get('/api/v1/user/me/', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.TEST_USER["username"])


class NotesTestCase(TestCase):
    def setUp(self):
        self.TEST_USER = {"username": "testuser", "password": "testpassword"}
        response = self.client.post('/api/v1/auth/signup/', data=self.TEST_USER)
        token = response.json()["token"]
        self.header = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        self.TEST_USER_2 = {"username": "testuser2", "password": "testpassword"}
        response = self.client.post('/api/v1/auth/signup/', data=self.TEST_USER_2)
        token = response.json()["token"]
        self.header_2 = {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_note_auth(self):
        """Test Note methods without auth"""
        response = self.client.post('/api/v1/note/', data={"title": "Lorem ipsum", "description": "Lorem iosum dolor sit amet"})
        self.assertEqual(response.status_code, 401)
        response = self.client.get('/api/v1/note/')
        self.assertEqual(response.status_code, 401)

    def test_create_note(self):
        title = "".join(random.choices(string.ascii_letters, k=6))
        response = self.client.post(
            '/api/v1/note/', 
            data={
                "title": title, 
                "description": "Lorem iosum dolor sit amet"
            }, 
            **self.header
        )
        self.assertEqual(response.status_code, 201)
        pk = response.json()["id"]

        # Test created note in listing
        response = self.client.get('/api/v1/note/', **self.header)
        self.assertContains(response, title)

        # Test created note detail
        response = self.client.get(f'/api/v1/note/{pk}/', **self.header)
        self.assertEqual(response.json()["id"], pk)
        self.assertEqual(response.json()["title"], title)

    def test_update_note(self):
        title = "".join(random.choices(string.ascii_letters, k=6))
        response = self.client.post(
            '/api/v1/note/', 
            data={
                "title": title, 
                "description": "Lorem iosum dolor sit amet"
            }, 
            **self.header
        )
        pk = response.json()["id"]

        new_title = "".join(random.choices(string.ascii_letters, k=6))
        new_desc = "".join(random.choices(string.ascii_letters, k=20))
        response = self.client.put(
            f'/api/v1/note/{pk}/', 
            data={
                "title": new_title, 
                "description": new_desc
            },
            content_type='application/json',
            **self.header
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/v1/note/{pk}/', **self.header)
        self.assertEqual(response.json()["title"], new_title)
        self.assertEqual(response.json()["description"], new_desc)

    def test_delete_note(self):
        title = "".join(random.choices(string.ascii_letters, k=6))
        response = self.client.post(
            '/api/v1/note/', 
            data={
                "title": title, 
                "description": "Lorem iosum dolor sit amet"
            }, 
            **self.header
        )
        pk = response.json()["id"]

        response = self.client.delete(f'/api/v1/note/{pk}/', **self.header)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/api/v1/note/{pk}/', **self.header)
        self.assertEqual(response.status_code, 404)

    def test_forbiden_note(self):
        # Create note for user
        title = "".join(random.choices(string.ascii_letters, k=6))
        response = self.client.post(
            '/api/v1/note/', 
            data={
                "title": title, 
                "description": "Lorem iosum dolor sit amet"
            }, 
            **self.header
        )
        pk = response.json()["id"]

        # Test get this note by another user
        response = self.client.get(f'/api/v1/note/{pk}/', **self.header_2)
        self.assertEqual(response.status_code, 404)
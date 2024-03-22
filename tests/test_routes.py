
from unittest.mock import patch
import unittest
from flask import json
from app import create_app, db
from tests.config import TestConfig
from app.models.user import User

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.auth_patcher = patch('app.auth.jwt_required', return_value=lambda: None)
        self.mock_auth = self.auth_patcher.start()

        user = User(username='existinguser', email='existing@example.com')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        self.auth_patcher.stop()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_route(self):
        response = self.client.post('/users', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('username', data)

    

if __name__ == '__main__':
    unittest.main()

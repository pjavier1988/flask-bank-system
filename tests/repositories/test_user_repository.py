
import unittest
from app import create_app, db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from tests.config import TestConfig
class UserRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.repo = UserRepository() 
        
        test_user = User(username='testuser1', email='test1@example.com')
        db.session.add(test_user)
        db.session.commit()
        self.test_user_id = test_user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_user(self):
        user = User(username='testuser', email='test@example.com')
        self.repo.add(user)
        retrieved = User.query.filter_by(username="testuser").first()
        self.assertEqual(retrieved.username, 'testuser')

    def test_get_user_by_id(self):
        user = self.repo.get_by_identifier(self.test_user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser1')

    def test_delete_user(self):
        user = self.repo.get_by_identifier(self.test_user_id)
        self.repo.remove(user)
        db.session.commit()
        user = self.repo.get_by_identifier(self.test_user_id)
        self.assertIsNone(user)

    def test_update_user(self):
        new_email = 'updated@example.com'
        user = self.repo.get_by_identifier(self.test_user_id)
        user.email = new_email
        db.session.commit()
        updated_user = self.repo.get_by_identifier(self.test_user_id)
        self.assertEqual(updated_user.email, new_email)

    def test_find_all_users(self):
        users = self.repo.list()
        self.assertTrue(len(users) > 0)
        found_test_user = any(user.id == self.test_user_id for user in users)
        self.assertTrue(found_test_user)

if __name__ == '__main__':
    unittest.main()

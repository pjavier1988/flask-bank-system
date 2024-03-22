import unittest
from unittest.mock import Mock
from app.services.user_service import UserService

class UserServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.user_repository_mock = Mock()
        self.user_service = UserService(self.user_repository_mock)

    def test_create_user_calls_add_on_repository(self):
        self.user_service.create_user('testuser', 'test@example.com')
        self.user_repository_mock.add.assert_called_once()

    def test_find_user_calls_get_by_username_on_repository(self):
        username = 'testuser'
        self.user_service.find_user(username)
        self.user_repository_mock.get_by_identifier.assert_called_once_with(username)

    def test_find_all_users_calls_list_on_repository(self):
        self.user_service.find_all_users()
        self.user_repository_mock.list.assert_called_once()

    def test_update_user_calls_update_on_repository(self):
        username = 'testuser'
        new_email = 'newemail@example.com'
        self.user_repository_mock.get_by_username.return_value = {'username': username, 'email': 'oldemail@example.com'}
        self.user_repository_mock.update.return_value = {'username': username, 'email': new_email}

        self.user_service.update_user(username, new_email)
        self.user_repository_mock.update.assert_called_once_with(username, new_email)

    def test_delete_user_calls_remove_on_repository(self):
        username = 'testuser'
        self.user_repository_mock.get_by_username.return_value = {'username': username, 'email': 'test@example.com'}

        self.user_service.delete_user(username)
        self.user_repository_mock.remove.assert_called_once()

if __name__ == '__main__':
    unittest.main()

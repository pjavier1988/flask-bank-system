from app.models.user import User;
from app.repositories.base_repository import BaseRepository
class UserService():

    def __init__(self, user_repository:BaseRepository) -> None:
        self.user_repository = user_repository

    def create_user(self, username, email, names):
        new_user = User(username=username, email=email, names=names)
        self.user_repository.add(new_user)
        return new_user

    def find_user(self, username):
        return self.user_repository.get_by_identifier(username)

    def find_all_users(self):
        return self.user_repository.list()

    def update_user(self, username,email):
        user = self.find_user(username)
        if user:
            updated_user = self.user_repository.update(username,email)
            return updated_user
        return None

    def delete_user(self, username):
        user = self.find_user(username)
        if user:
            self.user_repository.remove(user)
            return True
        return False
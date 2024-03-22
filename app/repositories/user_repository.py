from app.repositories.base_repository import BaseRepository
from app.models.user import User
from app.database import db

class UserRepository(BaseRepository):

    def add(self, user, commit= False):
        db.session.add(user)
        db.session.commit()

    def get_by_identifier(self, username):
        return User.query.filter_by(username = username).first()

    def list(self):
        return User.query.all()
    
    def update(self, identifier, new_value, commit= False):
        user = self.get_by_identifier(identifier)
        if user:
            user.email = new_value
            db.session.commit()
            return user
        return None

    def remove(self, user):
        db.session.delete(user)
        db.session.commit()

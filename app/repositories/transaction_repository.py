from app.repositories.base_repository import BaseRepository
from app.models.transaction import Transaction

from app.database import db

class TransactionRepository(BaseRepository):

    
    def add(self, transaction, commit= False):
        db.session.add(transaction)

    def get_by_identifier(self, account_number):
        return Transaction.query.get(account_number)


    def list(self):
        return Transaction.query.all()
    
    def update(self, identifier, new_value, commit= False):
        pass


    def remove(self, transaction):
        db.session.delete(transaction)
        db.session.commit()
    
    
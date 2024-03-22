
from app.repositories.base_repository import BaseRepository
from app.models.account import Account
from app.database import db

class AccountRepository(BaseRepository):

    def add(self,account,commit= False):
        new_account = db.session.add(account)
        if commit:
            db.session.commit()
        return new_account

    def get_by_identifier( self,account_number):
        return Account.query.filter_by(account_number = account_number).first()

    def list(self):
        return Account.query.all()
    
    def update( self, account, new_value, commit= False):
        account.balance = new_value
        return account


    def remove( self, user):
        db.session.delete(user)
        db.session.commit()
    
    def update_balance(self, account: Account, new_balance: float):
        account.balance = new_balance
        db.session.add(account)

from app.models.account import Account;
from app.repositories.base_repository import BaseRepository

class AccountService():

    def __init__(self, account_repository:BaseRepository) -> None:
        self.account_repository = account_repository

    def create_account(self, new_account):
        self.account_repository.add(new_account, commit= True)
        return new_account

    def find_account(self, account_number):
        return self.account_repository.get_by_identifier(account_number)

    def find_all_accounts(self):
        return self.account_repository.list()

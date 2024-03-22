
from app.repositories.base_repository import BaseRepository
from app.utils.decorators import transactional
from app.models.transaction import Transaction
from app.exceptions import SameAccountError, NegativeValueError,AccountNotExistsError, InsufficientFundsError

class TransactionService:
    
    def __init__(self, transaction_repo:BaseRepository, account_repo: BaseRepository) -> None:
        self.transaction_repo = transaction_repo
        self.account_repo = account_repo

   
    def validate_transfer(self, from_account_id: str, to_account_id: str, amount: float):
        if from_account_id == to_account_id:
            raise SameAccountError("Cannot transfer to the same account.")
        if amount <= 0:
            raise NegativeValueError("Amount must be positive.")
    

    def withdraw(self, account_number: str, amount: float):
        account = self.account_repo.get_by_identifier(account_number)
        if not account:
            raise AccountNotExistsError(f"Account {account_number} does not exist.")
        if account.balance < amount:
            raise InsufficientFundsError("Insufficient funds.")
        self.account_repo.update(account, account.balance - amount)

        transaction_object =  Transaction(amount=-amount, account_id=account.id, type='transfer')
        self.transaction_repo.add(transaction_object)

 
    def deposit(self, account_number: str, amount: float):
        account = self.account_repo.get_by_identifier(account_number)
        if not account:
            raise AccountNotExistsError(f"Account {account_number} does not exist.")
        self.account_repo.update(account, account.balance + amount)
        transaction_object =  Transaction(amount=amount, account_id=account.id, type='transfer')

        self.transaction_repo.add(transaction_object)


    @transactional
    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        self.validate_transfer(from_account_id, to_account_id, amount)
        self.withdraw(from_account_id, amount)
        self.deposit(to_account_id, amount)
        
        return True

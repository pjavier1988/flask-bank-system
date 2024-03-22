import unittest
from app import create_app 
from unittest.mock import MagicMock, patch
from app.services.transaction_service import TransactionService
from tests.config import TestConfig

class TestTransactionService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.mock_transaction_repo = MagicMock()
        self.mock_account_repo = MagicMock()

        self.service = TransactionService(transaction_repo=self.mock_transaction_repo, account_repo=self.mock_account_repo)
    
    def tearDown(self):
        self.app_ctx.pop()
        
    def test_validate_transfer_same_account(self):
        """Test transfer validation with the same from and to account IDs."""
        with self.assertRaises(ValueError):
            self.service.validate_transfer('123', '123', 100.0)

    def test_validate_transfer_negative_amount(self):
        """Test transfer validation with a negative amount."""
        with self.assertRaises(ValueError):
            self.service.validate_transfer('123', '456', -100.0)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawing with insufficient funds."""
        self.mock_account_repo.get_by_identifier.return_value = MagicMock(account_number='123', balance=50.0)

        with self.assertRaises(ValueError):
            self.service.withdraw('123', 100.0)


    @patch('app.services.transaction_service.transactional')
    def test_transfer(self, mock_transactional):
        """Test successful transfer from one account to another."""
        from_account = MagicMock(account_number='123', id=1, balance=200.0)
        to_account = MagicMock(account_number='456', id=2, balance=100.0)
        self.mock_account_repo.get_by_identifier.side_effect = [from_account, to_account]

        result = self.service.transfer('123', '456', 50.0)

        self.assertTrue(result)
        self.mock_account_repo.update.assert_any_call(from_account, 150.0)
        self.mock_account_repo.update.assert_any_call(to_account, 150.0)
        self.assertEqual(self.mock_transaction_repo.add.call_count, 2)

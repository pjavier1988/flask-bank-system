
from dependency_injector import containers, providers
from app.repositories.user_repository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.services.user_service import UserService
from app.services.transaction_service import TransactionService
from app.services.account_service import AccountService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository = providers.Factory(
        UserRepository,
    )

    account_repo = providers.Factory(
        AccountRepository,
    )
    transaction_repo = providers.Factory(
        TransactionRepository,
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    transaction_service = providers.Factory(
        TransactionService,
        account_repo=account_repo,
        transaction_repo=transaction_repo
    )

    account_service = providers.Factory(
        AccountService,
        account_repository=account_repo
    )

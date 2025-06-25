from abc import ABC, abstractmethod
from app.domain.model.user_identity import UserIdentity
from app.domain.model.account import Account
from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance


class Dsp2Client(ABC):
    @abstractmethod
    def get_token(self, username: str, password: str) -> str:
        """Authenticate user and return access token"""
        pass

    @abstractmethod
    def get_user_identity(self, token: str) -> UserIdentity:
        """Get user identity information"""
        pass

    @abstractmethod
    def get_accounts(self, token: str) -> list[Account]:
        """Get all user accounts"""
        pass

    @abstractmethod
    def get_account(self, token: str, account_id: str) -> Account:
        """Get specific account by ID"""
        pass

    @abstractmethod
    def get_balances(self, token: str, account_id: str) -> list[Balance]:
        """Get account balances"""
        pass

    @abstractmethod
    def get_transactions(
        self, token: str, account_id: str, page: int, limit: int
    ) -> list[Transaction]:
        """Get account transactions"""
        pass

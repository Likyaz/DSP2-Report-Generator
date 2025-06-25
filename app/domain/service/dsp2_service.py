from app.domain.port.dsp2_client import Dsp2Client
from app.domain.model.user_identity import UserIdentity
from app.domain.model.account import Account
from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance


class Dsp2Service:
    def __init__(self, dsp2_client: Dsp2Client, username: str, password: str):
        self.dsp2_client = dsp2_client
        self.token = self.dsp2_client.get_token(username, password)

    def get_user_identity(self) -> UserIdentity:
        return self.dsp2_client.get_user_identity(self.token)

    def get_accounts(self) -> list[Account]:
        return self.dsp2_client.get_accounts(self.token)

    def get_account(self, account_id: str) -> Account:
        return self.dsp2_client.get_account(self.token, account_id)

    def get_balances(self, account_id: str) -> list[Balance]:
        return self.dsp2_client.get_balances(self.token, account_id)

    def get_all_transactions(
        self, account_id: str, count: int = 100
    ) -> list[Transaction]:
        transactions = []
        page = 1
        while True:
            page_transactions = self.dsp2_client.get_transactions(
                self.token, account_id, page=page, count=count
            )
            transactions.extend(page_transactions)
            if len(page_transactions) < count:
                break
            page += 1
        return transactions

    def iter_all_transactions(self, account_id: str, count: int = 100):
        page = 1
        while True:
            transactions = self.dsp2_client.get_transactions(
                self.token, account_id, page=page, count=count
            )
            if not transactions:
                break
            for transaction in transactions:
                yield transaction
            if len(transactions) < count:
                break
            page += 1

    def get_transactions(
        self, account_id: str, page: int = 1, count: int = 100
    ) -> list[Transaction]:
        return self.dsp2_client.get_transactions(self.token, account_id, page, count)

import requests

from app.domain.port.dsp2_client import Dsp2Client
from app.domain.model.user_identity import UserIdentity
from app.domain.model.account import Account
from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance
from app.adapter.serializers.account_serializer import AccountSerializer
from app.adapter.serializers.user_identity_serializer import UserIdentitySerializer
from app.adapter.serializers.balance_serializer import BalanceSerializer
from app.adapter.serializers.transaction_serializer import TransactionSerializer


class Dsp2ApiAdapter(Dsp2Client):
    BASE_URL = "https://dsp2-technical-test.iliad78.net"

    def __init__(self):
        self.session = requests.Session()

    def get_token(self, username: str, password: str) -> str:
        auth_url = f"{self.BASE_URL}/oauth/token"

        payload = {"username": username, "password": password, "scope": "stet"}

        response = self.session.post(auth_url, data=payload)
        response.raise_for_status()

        data = response.json()
        return data["access_token"]

    def get_user_identity(self, token: str) -> UserIdentity:
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(f"{self.BASE_URL}/stet/identity", headers=headers)
        response.raise_for_status()

        data = response.json()
        return UserIdentitySerializer.from_api_response(data)

    def get_accounts(self, token: str) -> list[Account]:
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(f"{self.BASE_URL}/stet/account", headers=headers)
        response.raise_for_status()

        data = response.json()
        return AccountSerializer.from_api_list(data)

    def get_account(self, token: str, account_id: str) -> Account:
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(
            f"{self.BASE_URL}/stet/account/{account_id}", headers=headers
        )
        response.raise_for_status()

        data = response.json()
        return AccountSerializer.from_api_response(data)

    def get_balances(self, token: str, account_id: str) -> list[Balance]:
        headers = {"Authorization": f"Bearer {token}"}
        response = self.session.get(
            f"{self.BASE_URL}/stet/account/{account_id}/balance", headers=headers
        )
        response.raise_for_status()

        data = response.json()
        return BalanceSerializer.from_api_list(data)

    def get_transactions(
        self, token: str, account_id: str, page: int, count: int
    ) -> list[Transaction]:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"page": page, "count": count}
        response = self.session.get(
            f"{self.BASE_URL}/stet/account/{account_id}/transaction",
            headers=headers,
            params=params,
        )
        response.raise_for_status()

        data = response.json()
        return TransactionSerializer.from_api_list(data)

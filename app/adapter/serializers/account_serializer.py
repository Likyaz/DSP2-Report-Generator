from typing import Dict, Any
from app.domain.model.account import Account


class AccountSerializer:
    """Serializes DSP2 API account data to domain Account objects"""

    @staticmethod
    def from_api_response(api_data: Dict[str, Any]) -> Account:
        """Convert API response to Account domain object"""
        return Account(
            id=api_data["id"],
            type=Account.Type[api_data["type"]],
            usage=Account.Usage[api_data["usage"]],
            iban=api_data["iban"],
            name=api_data["name"],
            currency=api_data["currency"],
        )

    @staticmethod
    def from_api_list(api_data_list: list[Dict[str, Any]]) -> list[Account]:
        """Convert list of API responses to Account domain objects"""
        return [
            AccountSerializer.from_api_response(account_data)
            for account_data in api_data_list
        ]

    @staticmethod
    def to_dict(account: Account) -> Dict[str, Any]:
        """Convert Account domain object to dictionary"""
        return {
            "id": account.id,
            "type": account.type.value,
            "usage": account.usage.value,
            "iban": account.iban,
            "name": account.name,
            "currency": account.currency,
        }

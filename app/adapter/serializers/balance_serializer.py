from typing import Dict, Any
from app.domain.model.balance import Balance


class BalanceSerializer:
    """Serializes DSP2 API balance data to domain Balance objects"""

    @staticmethod
    def from_api_list(api_data_list: list[Dict[str, Any]]) -> list[Balance]:
        """Convert API response to Balance domain object"""
        return [
            Balance(
                id=api_data["id"],
                name=api_data["name"],
                amount=api_data["amount"],
                currency=api_data["currency"],
                type=Balance.Type[api_data["type"]],
            )
            for api_data in api_data_list
        ]

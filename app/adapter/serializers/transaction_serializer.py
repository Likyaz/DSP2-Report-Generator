from typing import Dict, Any
from app.domain.model.transaction import Transaction


class TransactionSerializer:
    """Serializes DSP2 API transaction data to domain Transaction objects"""

    @staticmethod
    def from_api_list(api_data_list: list[Dict[str, Any]]) -> list[Transaction]:
        """Convert API response to Transaction domain object"""
        return [
            Transaction(
                id=api_data["id"],
                label=api_data["label"],
                amount=api_data["amount"],
                crdt_dbit_indicator=Transaction.CreditDebitIndicator[
                    api_data["crdt_dbit_indicator"]
                ],
                status=Transaction.Status[api_data["status"]],
                currency=api_data["currency"],
                date_operation=api_data["date_operation"],
                date_processed=api_data["date_processed"],
            )
            for api_data in api_data_list
        ]

    @staticmethod
    def to_dict(transaction: Transaction) -> Dict[str, Any]:
        """Convert Transaction domain object to dictionary"""
        return {
            "id": transaction.id,
            "label": transaction.label,
            "amount": transaction.amount,
            "crdt_dbit_indicator": transaction.crdt_dbit_indicator.value,
            "status": transaction.status.value,
            "currency": transaction.currency,
            "date_operation": transaction.date_operation,
            "date_processed": transaction.date_processed,
        }

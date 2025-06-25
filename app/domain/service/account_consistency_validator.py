from typing import List

from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance


class AccountConsistencyValidator:
    @staticmethod
    def validate(token: str, adapter) -> List[str]:
        errors = []
        accounts = adapter.get_accounts(token)
        for account in accounts:
            balances = adapter.get_balances(token, account.id)
            balance = next((b for b in balances if b.type.name == "CLBD"), None)
            if not balance:
                errors.append(f"No CLBD balance found for account {account.id}")
                continue

            total = 0
            sum_credits = 0
            sum_debits = 0
            page = 1
            while True:
                transactions = adapter.get_transactions(
                    token, account.id, page=page, count=100
                )
                for transaction in transactions:
                    if transaction.status != Transaction.Status.BOOK:
                        continue
                    if (
                        transaction.crdt_dbit_indicator
                        == Transaction.CreditDebitIndicator.DBIT
                    ):
                        sum_debits += transaction.amount / 100
                        total -= transaction.amount / 100
                    elif (
                        transaction.crdt_dbit_indicator
                        == Transaction.CreditDebitIndicator.CRDT
                    ):
                        sum_credits += transaction.amount / 100
                        total += transaction.amount / 100
                if len(transactions) < 100:
                    break
                page += 1

            if total != balance.amount / 100:
                errors.append(
                    f"Inconsistency for account {account.id}: sum(transactions)={total:.2f} != balance={balance.amount/100:.2f}, sum(debits)={sum_debits:.2f}, sum(credits)={sum_credits:.2f}"
                )
        return errors

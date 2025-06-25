from typing import List

from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance
from app.domain.service.dsp2_service import Dsp2Service


class AccountConsistencyValidator:
    @staticmethod
    def validate(dsp2_service: Dsp2Service) -> List[str]:
        errors = []
        accounts = dsp2_service.get_accounts()
        for account in accounts:
            balances = dsp2_service.get_balances(account.id)
            balance = next((b for b in balances if b.type.name == "CLBD"), None)
            if not balance:
                errors.append(f"No CLBD balance found for account {account.id}")
                continue

            total = 0
            sum_credits = 0
            sum_debits = 0
            for transaction in dsp2_service.iter_all_transactions(
                account.id, count=100
            ):
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

            if total != balance.amount / 100:
                errors.append(
                    f"Inconsistency for account {account.id}: sum(transactions)={total:.2f} != balance={balance.amount/100:.2f}, sum(debits)={sum_debits:.2f}, sum(credits)={sum_credits:.2f}"
                )
        return errors

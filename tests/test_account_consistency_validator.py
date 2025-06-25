import pytest
from app.domain.service.account_consistency_validator import AccountConsistencyValidator
from app.domain.model.account import Account
from app.domain.model.balance import Balance
from app.domain.model.transaction import Transaction
from unittest.mock import MagicMock
from datetime import datetime


class DummyAdapter:
    def get_accounts(self, token):
        return [
            Account(
                id="acc1",
                type=Account.Type.CACC,
                usage=Account.Usage.PRIV,
                iban="iban1",
                name="Compte 1",
                currency="EUR",
            )
        ]

    def get_balances(self, token, account_id):
        return [
            Balance(
                id="bal1",
                name="balance1",
                amount=1000,
                currency="EUR",
                type=Balance.Type.CLBD,
            )
        ]

    def get_transactions(self, token, account_id, page, count):
        if page == 1:
            return [
                Transaction(
                    id="tx1",
                    label="credit",
                    amount=3000,
                    crdt_dbit_indicator=Transaction.CreditDebitIndicator.CRDT,
                    status=Transaction.Status.BOOK,
                    currency="EUR",
                    date_operation=datetime(2024, 1, 1, 12, 0, 0),
                    date_processed=datetime(2024, 1, 2, 12, 0, 0),
                ),
                Transaction(
                    id="tx2",
                    label="debit",
                    amount=2000,
                    crdt_dbit_indicator=Transaction.CreditDebitIndicator.DBIT,
                    status=Transaction.Status.BOOK,
                    currency="EUR",
                    date_operation=datetime(2024, 1, 3, 12, 0, 0),
                    date_processed=datetime(2024, 1, 4, 12, 0, 0),
                ),
            ]
        return []


def test_account_consistency_validator_ok():
    adapter = DummyAdapter()
    token = "token"
    errors = AccountConsistencyValidator.validate(token, adapter)
    assert errors == []


def test_account_consistency_validator_inconsistent():
    class BadAdapter(DummyAdapter):
        def get_balances(self, token, account_id):
            return [
                Balance(
                    id="bal1",
                    name="balance1",
                    amount=10000,
                    currency="EUR",
                    type=Balance.Type.CLBD,
                )
            ]

    adapter = BadAdapter()
    token = "token"
    errors = AccountConsistencyValidator.validate(token, adapter)
    assert len(errors) == 1

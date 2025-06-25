import pytest
from app.domain.service.account_consistency_validator import AccountConsistencyValidator
from app.domain.model.account import Account
from app.domain.model.balance import Balance
from app.domain.model.transaction import Transaction
from datetime import datetime


class DummyDsp2Service:
    def get_accounts(self):
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

    def get_balances(self, account_id):
        return [
            Balance(
                id="bal1",
                name="balance1",
                amount=1000,
                currency="EUR",
                type=Balance.Type.CLBD,
            )
        ]

    def iter_all_transactions(self, account_id, page=1, count=100):
        yield Transaction(
            id="tx1",
            label="credit",
            amount=3000,
            crdt_dbit_indicator=Transaction.CreditDebitIndicator.CRDT,
            status=Transaction.Status.BOOK,
            currency="EUR",
            date_operation=datetime(2024, 1, 1, 12, 0, 0),
            date_processed=datetime(2024, 1, 2, 12, 0, 0),
        )
        yield Transaction(
            id="tx2",
            label="debit",
            amount=2000,
            crdt_dbit_indicator=Transaction.CreditDebitIndicator.DBIT,
            status=Transaction.Status.BOOK,
            currency="EUR",
            date_operation=datetime(2024, 1, 3, 12, 0, 0),
            date_processed=datetime(2024, 1, 4, 12, 0, 0),
        )


class DummyBadDsp2Service(DummyDsp2Service):
    def get_balances(self, account_id):
        return [
            Balance(
                id="bal1",
                name="balance1",
                amount=10000,
                currency="EUR",
                type=Balance.Type.CLBD,
            )
        ]


def test_account_consistency_validator_ok():
    service = DummyDsp2Service()
    errors = AccountConsistencyValidator.validate(service)
    assert errors == []


def test_account_consistency_validator_inconsistent():
    service = DummyBadDsp2Service()
    errors = AccountConsistencyValidator.validate(service)
    assert len(errors) == 1
    assert "Inconsistency" in errors[0]

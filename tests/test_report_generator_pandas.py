import pytest
import json
import pandas as pd
from datetime import datetime, date
from app.adapter.report_generator_pandas import ReportGeneratorPandas
from app.domain.model.report import Report
from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance
from app.domain.model.account import Account
from app.domain.model.user_identity import UserIdentity


@pytest.fixture
def sample_transactions():
    return [
        Transaction(
            id="transaction1",
            label="Transaction 1",
            amount=1000,
            crdt_dbit_indicator=Transaction.CreditDebitIndicator.CRDT,
            status=Transaction.Status.BOOK,
            currency="EUR",
            date_operation=datetime(2024, 1, 15, 10, 0, 0),
            date_processed=datetime(2024, 1, 16, 10, 0, 0),
        ),
        Transaction(
            id="transaction2",
            label="Transaction 2",
            amount=500,
            crdt_dbit_indicator=Transaction.CreditDebitIndicator.DBIT,
            status=Transaction.Status.BOOK,
            currency="EUR",
            date_operation=datetime(2024, 1, 20, 10, 0, 0),
            date_processed=datetime(2024, 1, 21, 10, 0, 0),
        ),
    ]


@pytest.fixture
def sample_report(sample_transactions):
    user_identity = UserIdentity(
        id="user1",
        prefix=UserIdentity.Prefix.MIST,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
    )
    account = Account(
        id="acc1",
        type=Account.Type.CACC,
        usage=Account.Usage.PRIV,
        iban="FR123456789",
        name="Compte Principal",
        currency="EUR",
    )
    balance = Balance(
        id="bal1",
        name="Solde",
        amount=5000,
        currency="EUR",
        type=Balance.Type.CLBD,
    )
    return Report(
        date_generated=datetime(2024, 1, 25, 12, 0, 0),
        date_start=date(2024, 1, 1),
        date_end=date(2024, 1, 31),
        user_identity=user_identity,
        account=account,
        balance=balance,
        transactions=sample_transactions,
    )


@pytest.fixture
def report_generator():
    return ReportGeneratorPandas()


def test_generate_json(report_generator, sample_report):
    result = report_generator.generate_json(sample_report)
    data = json.loads(result)

    assert data["date_generated"] == "2024-01-25T12:00:00"
    assert data["date_start"] == "2024-01-01"
    assert data["date_end"] == "2024-01-31"
    assert data["user_name"] == "mister John Doe"
    assert data["account"]["id"] == "acc1"
    assert data["balance"]["id"] == "bal1"
    assert len(data["transactions"]) == 2
    assert data["transactions"][0]["id"] == "transaction1"
    assert data["transactions"][1]["id"] == "transaction2"


def test_generate_csv(report_generator, sample_report):
    result = report_generator.generate_csv(sample_report)

    assert "id" in result
    assert "label" in result
    assert "amount" in result
    assert "crdt_dbit_indicator" in result
    assert "status" in result
    assert "currency" in result
    assert "transaction1" in result
    assert "transaction2" in result
    assert "Transaction 1" in result
    assert "Transaction 2" in result


def test_filter_transactions_by_date():
    from app.adapter.report_generator_pandas import _filter_transactions_by_date

    transactions_data = [
        {"date_operation": datetime(2024, 1, 15, 10, 0, 0), "amount": 100},
        {"date_operation": datetime(2024, 1, 20, 10, 0, 0), "amount": 200},
        {
            "date_operation": datetime(2024, 2, 15, 10, 0, 0),
            "amount": 300,
        },
    ]
    df = pd.DataFrame(transactions_data)
    filtered_df = _filter_transactions_by_date(df, date(2024, 1, 1), date(2024, 1, 31))

    assert len(filtered_df) == 2
    assert filtered_df.iloc[0]["amount"] == 100
    assert filtered_df.iloc[1]["amount"] == 200


def test_generate_json_with_empty_transactions(report_generator, sample_report):
    sample_report.transactions = []
    result = report_generator.generate_json(sample_report)
    data = json.loads(result)
    assert data["transactions"] == []


def test_generate_csv_with_empty_transactions(report_generator, sample_report):
    sample_report.transactions = []
    result = report_generator.generate_csv(sample_report)
    assert result.strip() == ""

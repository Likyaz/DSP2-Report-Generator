from app.domain.port.report_generator import ReportGenerator
from app.adapter.serializers.account_serializer import AccountSerializer
from app.adapter.serializers.balance_serializer import BalanceSerializer
from app.adapter.serializers.transaction_serializer import TransactionSerializer

import pandas as pd
from io import StringIO
import json


class ReportGeneratorPandas(ReportGenerator):
    def generate_json(self, report):
        transactions_data = [
            TransactionSerializer.to_dict(t) for t in report.transactions
        ]
        transactions_df = pd.DataFrame(transactions_data)
        transactions_df = _filter_transactions_by_date(
            transactions_df, report.date_start, report.date_end
        )
        user_name = f"{report.user_identity.prefix.value} {report.user_identity.first_name} {report.user_identity.last_name}"

        if transactions_df.empty:
            transactions_list = []
        else:
            transactions_df["date_operation"] = pd.to_datetime(
                transactions_df["date_operation"]
            ).dt.strftime("%Y-%m-%d")
            transactions_df["date_processed"] = pd.to_datetime(
                transactions_df["date_processed"]
            ).dt.strftime("%Y-%m-%dT%H:%M:%S")
            transactions_list = transactions_df.to_dict(orient="records")

        result = {
            "date_generated": report.date_generated.isoformat(),
            "date_start": report.date_start.isoformat(),
            "date_end": report.date_end.isoformat(),
            "user_name": user_name,
            "account": AccountSerializer.to_dict(report.account),
            "balance": BalanceSerializer.to_dict(report.balance),
            "transactions": transactions_list,
        }
        print(result)
        return json.dumps(result)

    def generate_csv(self, report):
        transactions_data = [t for t in report.transactions]
        transactions_df = pd.DataFrame(transactions_data)
        transactions_df = _filter_transactions_by_date(
            transactions_df, report.date_start, report.date_end
        )
        output = StringIO()
        transactions_df.to_csv(output, index=False)
        return output.getvalue()


def _filter_transactions_by_date(transactions, date_start, date_end):
    if transactions.empty:
        return transactions

    if transactions["date_operation"].dtype == "object":
        if hasattr(transactions["date_operation"].iloc[0], "date"):
            date_operation_col = transactions["date_operation"]
        else:
            date_operation_col = pd.to_datetime(transactions["date_operation"])
    else:
        date_operation_col = transactions["date_operation"]

    mask = (date_operation_col >= pd.to_datetime(date_start)) & (
        date_operation_col <= pd.to_datetime(date_end)
    )
    return transactions.loc[mask]

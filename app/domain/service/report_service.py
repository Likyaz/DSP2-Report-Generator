from datetime import datetime, date

from app.adapter.get_report_generator import get_report_generator
from app.domain.model.report import Report
from app.domain.port.report_generator import ReportGenerator
from app.domain.service.dsp2_service import Dsp2Service


class ReportService:
    def __init__(self, dsp2_service: Dsp2Service):
        self.dsp2_service = dsp2_service
        self.report_generator: ReportGenerator = get_report_generator()

    def generate_report_json(
        self,
        account_id: str,
        date_start: date,
        date_end: date,
    ) -> str:
        report = self._generate_report(
            account_id,
            date_start,
            date_end,
        )
        return self.report_generator.generate_json(report)

    def generate_report_csv(
        self,
        account_id: str,
        date_start: date,
        date_end: date,
    ) -> str:
        report = self._generate_report(
            account_id,
            date_start,
            date_end,
        )
        return self.report_generator.generate_csv(report)

    def _generate_report(
        self,
        account_id: str,
        date_start: date,
        date_end: date,
    ) -> Report:
        account = self.dsp2_service.get_account(account_id)
        balances = self.dsp2_service.get_balances(account_id)
        balance = balances[0]
        user_identity = self.dsp2_service.get_user_identity()
        transactions = self.dsp2_service.get_all_transactions(account_id)

        return Report(
            date_generated=datetime.now(),
            date_start=date_start,
            date_end=date_end,
            user_identity=user_identity,
            account=account,
            balance=balance,
            transactions=transactions,
        )

from abc import ABC, abstractmethod

from app.domain.model.account import Account
from app.domain.model.balance import Balance
from app.domain.model.transaction import Transaction
from app.domain.model.report import Report


class ReportGenerator(ABC):
    @abstractmethod
    def generate_json(self, report: Report) -> str:
        pass

    @abstractmethod
    def generate_csv(self, report: Report) -> str:
        pass

from datetime import datetime
from enum import Enum
from dataclasses import dataclass


@dataclass
class Transaction:
    class CreditDebitIndicator(Enum):
        CRDT = "credit"
        DBIT = "debit"

    class Status(Enum):
        BOOK = "booked"
        PDNG = "pending"
        FUTR = "future"
        INFO = "Informational"

    id: str
    label: str
    amount: int
    crdt_dbit_indicator: CreditDebitIndicator
    status: Status
    currency: str
    date_operation: datetime
    date_processed: datetime | None

from datetime import datetime, date
from dataclasses import dataclass

from app.domain.model.transaction import Transaction
from app.domain.model.balance import Balance
from app.domain.model.account import Account
from app.domain.model.user_identity import UserIdentity


@dataclass
class Report:
    date_generated: datetime
    date_start: date
    date_end: date
    user_identity: UserIdentity
    account: Account
    balance: Balance
    transactions: list[Transaction]

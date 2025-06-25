from enum import Enum
from dataclasses import dataclass


@dataclass
class Balance:
    class Type(Enum):
        CLBD = "closing booked"
        XPCD = "expected"
        VALU = "value"
        ITAV = "interim available"
        PRCD = "projected"
        OTHR = "other"

    id: str
    name: str
    amount: int
    currency: str
    type: Type

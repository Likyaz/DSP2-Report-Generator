from enum import Enum
from dataclasses import dataclass


@dataclass
class Account:
    class Type(Enum):
        CACC = "current"
        CARD = "card"

    class Usage(Enum):
        PRIV = "private"
        ORGA = "organization"

    id: str
    type: Type
    usage: Usage
    iban: str
    name: str
    currency: str | None

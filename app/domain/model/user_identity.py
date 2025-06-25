from datetime import date
from enum import Enum
from dataclasses import dataclass


@dataclass
class UserIdentity:
    class Prefix(Enum):
        DOCT = "doctor"
        MIST = "mister"
        MADM = "missus"
        MISS = "ms"

    id: str
    prefix: Prefix
    first_name: str
    last_name: str
    date_of_birth: date

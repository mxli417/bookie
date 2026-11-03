from dataclasses import dataclass
from enum import Enum
from typing import List


class Outcome(str, Enum):
    HOME = "HOME"
    DRAW = "DRAW"
    AWAY = "AWAY"


@dataclass(frozen=True)
class Market:
    market_id: str
    outcomes: List[Outcome]


@dataclass(frozen=True)
class Price:
    odds: float


@dataclass(frozen=True)
class Bet:
    bet_id: str
    market_id: str
    outcome: Outcome
    stake: float  # total bet amount set forth by the gambler
    odds: float  # locked-in odds at acceptance time

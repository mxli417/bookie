"""
    Bet checking for our bookie engine. Adding bets to the book 
    is only allowed if the minimum value of the worst case event
    calculation stays above the minimum PnL value. An alternative 
    to that would be to requote on the outcomes, i.e. lower the
    quotes on the outcomes to keep the minimum PnL in check. 
"""

from dataclasses import dataclass
from typing import Tuple
from bookie.engine.types import Bet
from bookie.engine.risk import RiskBook

@dataclass(frozen=True)
class AcceptDecision:
    accepted: bool
    reason: str

def check_bet(book: RiskBook, bet: Bet, min_worst_case_pnl: float) -> AcceptDecision:
    # simulate adding bet
    tmp = RiskBook(stakes=dict(book.stakes), liability=dict(book.liability))
    tmp.add_bet(bet)
    worstcase = tmp.worst_case_pnl()
    if min(worstcase.values()) < min_worst_case_pnl:
        return AcceptDecision(
            False, 
            f"RISK_LIMIT: worst_case={min(worstcase.values()):.2f}"
        )
    return AcceptDecision(True, "OK")

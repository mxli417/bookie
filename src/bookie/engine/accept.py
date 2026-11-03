"""
Bet checking for our bookie engine. Adding bets to the book
is only allowed if the minimum value of the worst case event
calculation stays above the minimum PnL value. An alternative
to that would be to requote on the outcomes, i.e. lower the
quotes on the outcomes to keep the minimum PnL in check.
"""

from dataclasses import dataclass

from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet


@dataclass(frozen=True)
class AcceptDecision:
    accepted: bool
    reason: str
    projected_worst_case_pnl: float
    risk_floor: float


def check_bet(book: RiskBook, bet: Bet, min_worst_case_pnl: float) -> AcceptDecision:
    # simulate adding bet
    tmp = RiskBook(stakes=dict(book.stakes), liability=dict(book.liability))
    tmp.add_bet(bet)
    worstcase = tmp.worst_case_pnl()
    projected_worst_case = min(worstcase.values())
    if projected_worst_case < min_worst_case_pnl:
        return AcceptDecision(
            accepted=False,
            reason=(
                f"Projected worst-case PnL {projected_worst_case:.2f} "
                f"breaches risk floor {min_worst_case_pnl:.2f}."
            ),
            projected_worst_case_pnl=projected_worst_case,
            risk_floor=min_worst_case_pnl,
        )
    return AcceptDecision(
        accepted=True,
        reason=(
            f"Projected worst-case PnL {projected_worst_case:.2f} "
            f"meets risk floor {min_worst_case_pnl:.2f}."
        ),
        projected_worst_case_pnl=projected_worst_case,
        risk_floor=min_worst_case_pnl,
    )

"""
Settlement of the book. Given the match outcome, the book is settled
and total profit and loss calculated for the bookie and the individual bet.
"""

from typing import List, Tuple

from .types import Bet, Outcome


def settle(bets: List[Bet], result: Outcome) -> Tuple[float, List[Tuple[str, float]]]:
    total = 0.0
    per = []
    for b in bets:
        if b.outcome == result:
            pnl = -b.stake * (b.odds - 1.0)
        else:
            pnl = b.stake
        total += pnl
        per.append((b.bet_id, pnl))
    return total, per

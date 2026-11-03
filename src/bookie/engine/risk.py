"""
    Bookmaker miniaturized book risk calculation. For the three allowed
    outcomes here (home wins, away wins, the match is a draw) we track 
    the stakes (bet amount set forth by gamblers) and the liabilities 
    (stake * odds of the outcome minus the initial stake) to have an 
    overview on how much money could be lost by the bookie. Worst case
    PnL (Profit and Loss) tracks the outcomes for all three elementary 
    events, calculating the profit or losses on each bet outcome. 
    Bookie profit is equal to the sum of stakes of the loosing outcomes
    minus the liability on the winning outcome.
"""

from dataclasses import dataclass
from typing import Dict
from bookie.engine.types import Outcome, Bet

@dataclass
class RiskBook:
    # total stakes per outcome and total liabilities
    stakes: Dict[Outcome, float]  
    liability: Dict[Outcome, float]

    @staticmethod
    def empty(outcomes):
        return RiskBook(
            stakes={o: 0.0 for o in outcomes},
            liability={o: 0.0 for o in outcomes},
        )

    def add_bet(self, bet: Bet):
        self.stakes[bet.outcome] += bet.stake
        # payout - stake for winning bets
        self.liability[bet.outcome] += bet.stake * (bet.odds - 1.0)

    def worst_case_pnl(self) -> Dict[Outcome, float]:
        total_stakes = sum(self.stakes.values())
        pnl = {}
        for o in self.stakes:
            losing_stakes = total_stakes - self.stakes[o]
            pnl[o] = losing_stakes - self.liability[o]
        return pnl

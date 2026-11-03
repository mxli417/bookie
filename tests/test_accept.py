import pytest

from bookie.engine.accept import check_bet
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome


@pytest.fixture
def empty_book() -> RiskBook:
    return RiskBook.empty([Outcome.HOME, Outcome.DRAW, Outcome.AWAY])


def test_check_bet_accepts_at_exact_risk_floor_without_mutating_book(
    empty_book: RiskBook,
):
    bet = Bet("B1", "M1", Outcome.HOME, stake=10.0, odds=2.0)

    decision = check_bet(empty_book, bet, min_worst_case_pnl=-10.0)

    assert decision.accepted is True
    assert decision.reason == "OK"
    assert sum(empty_book.stakes.values()) == 0.0
    assert sum(empty_book.liability.values()) == 0.0


def test_check_bet_rejects_when_new_worst_case_breaches_floor(
    empty_book: RiskBook,
):
    bet = Bet("B1", "M1", Outcome.HOME, stake=10.0, odds=2.0)

    decision = check_bet(empty_book, bet, min_worst_case_pnl=-9.99)

    assert decision.accepted is False
    assert decision.reason == "RISK_LIMIT: worst_case=-10.00"
    assert sum(empty_book.stakes.values()) == 0.0


def test_accepted_bet_can_be_added_by_caller(empty_book: RiskBook):
    bet = Bet("B1", "M1", Outcome.AWAY, stake=20.0, odds=3.0)

    decision = check_bet(empty_book, bet, min_worst_case_pnl=-40.0)
    if decision.accepted:
        empty_book.add_bet(bet)

    assert empty_book.stakes[Outcome.AWAY] == pytest.approx(20.0)
    assert empty_book.liability[Outcome.AWAY] == pytest.approx(40.0)

import pytest

from bookie.engine.risk import RiskBook
from bookie.engine.settlement import settle
from bookie.engine.types import Bet, Outcome


@pytest.fixture
def bets() -> list[Bet]:
    return [
        Bet("B1", "M1", Outcome.HOME, stake=10.0, odds=2.0),
        Bet("B2", "M1", Outcome.DRAW, stake=20.0, odds=3.0),
        Bet("B3", "M1", Outcome.AWAY, stake=5.0, odds=4.0),
    ]


def test_settle_returns_bookmaker_total_and_per_bet_pnl(bets: list[Bet]):
    total, per_bet = settle(bets, Outcome.HOME)

    assert total == pytest.approx(15.0)
    assert per_bet == [("B1", -10.0), ("B2", 20.0), ("B3", 5.0)]


@pytest.mark.parametrize("result", list(Outcome))
def test_settlement_matches_risk_surface_for_every_outcome(
    bets: list[Bet], result: Outcome
):
    book = RiskBook.empty(list(Outcome))
    for bet in bets:
        book.add_bet(bet)

    total, _ = settle(bets, result)

    assert total == pytest.approx(book.worst_case_pnl()[result])


def test_empty_book_settles_to_zero():
    assert settle([], Outcome.HOME) == (0.0, [])

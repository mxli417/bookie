import pytest

from bookie.engine.types import Outcome, Bet
from bookie.engine.risk import RiskBook


def test_riskbook_empty_initializes_zero_state():
    outcomes = [Outcome.HOME, Outcome.DRAW, Outcome.AWAY]

    book = RiskBook.empty(outcomes)

    # All stakes and liabilities start at 0.0
    for o in outcomes:
        assert o in book.stakes
        assert o in book.liability
        assert book.stakes[o] == 0.0
        assert book.liability[o] == 0.0


def test_add_bet_updates_stakes_and_liability_correctly():
    outcomes = [Outcome.HOME, Outcome.DRAW, Outcome.AWAY]
    book = RiskBook.empty(outcomes)

    bet = Bet(
        bet_id="B1",
        market_id="M1",
        outcome=Outcome.HOME,
        stake=10.0,
        odds=2.5,  # liability = stake * (odds - 1) = 10 * 1.5 = 15
    )

    book.add_bet(bet)

    assert book.stakes[Outcome.HOME] == pytest.approx(10.0)
    assert book.liability[Outcome.HOME] == pytest.approx(15.0)

    # Other outcomes should remain at zero
    assert book.stakes[Outcome.DRAW] == 0.0
    assert book.stakes[Outcome.AWAY] == 0.0
    assert book.liability[Outcome.DRAW] == 0.0
    assert book.liability[Outcome.AWAY] == 0.0


def test_worst_case_pnl_matches_hand_calculation():
    """
    Construct a small hand-checkable scenario:

    Outcomes: HOME, DRAW, AWAY
    Bets:
      B1: HOME, stake=10, odds=2.0 -> liability 10
      B2: DRAW, stake=20, odds=3.0 -> liability 40
      B3: AWAY, stake=30, odds=4.0 -> liability 90

    Total stakes = 60

    If HOME wins:
      losing stakes = 60 - 10 = 50
      pnl_home = 50 - 10 = 40

    If DRAW wins:
      losing stakes = 60 - 20 = 40
      pnl_draw = 40 - 40 = 0

    If AWAY wins:
      losing stakes = 60 - 30 = 30
      pnl_away = 30 - 90 = -60
    """
    outcomes = [Outcome.HOME, Outcome.DRAW, Outcome.AWAY]
    book = RiskBook.empty(outcomes)

    bets = [
        Bet("B1", "M1", Outcome.HOME, 10.0, 2.0),
        Bet("B2", "M1", Outcome.DRAW, 20.0, 3.0),
        Bet("B3", "M1", Outcome.AWAY, 30.0, 4.0),
    ]

    for b in bets:
        book.add_bet(b)

    worst = book.worst_case_pnl()

    assert worst[Outcome.HOME] == pytest.approx(40.0)
    assert worst[Outcome.DRAW] == pytest.approx(0.0)
    assert worst[Outcome.AWAY] == pytest.approx(-60.0)

    # AWAY should be the true worst case here
    assert min(worst.values()) == pytest.approx(-60.0)


def test_worst_case_pnl_gets_worse_when_adding_liability():
    """
    Check monotonicity: if we add an extra bet on one outcome,
    the worst-case PnL for that outcome should not improve.
    """
    outcomes = [Outcome.HOME, Outcome.DRAW, Outcome.AWAY]
    book = RiskBook.empty(outcomes)

    # Start with one moderate bet on HOME
    base_bet = Bet("B1", "M1", Outcome.HOME, 10.0, 2.0)
    book.add_bet(base_bet)

    worst_before = book.worst_case_pnl()[Outcome.HOME]

    # Add another larger bet on HOME, increasing liability
    extra_bet = Bet("B2", "M1", Outcome.HOME, 50.0, 3.0)
    book.add_bet(extra_bet)

    worst_after = book.worst_case_pnl()[Outcome.HOME]

    # Worst-case for HOME should be <= (i.e. more negative than) before
    assert worst_after <= worst_before

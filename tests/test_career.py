import pytest

from bookie.career import (
    career_odds,
    career_probabilities,
    settlement_rows,
    summarize_book,
)
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome


def test_career_probabilities_form_binary_distribution():
    probabilities = career_probabilities(0.65)

    assert probabilities == {Outcome.HOME: 0.65, Outcome.AWAY: 0.35}
    assert sum(probabilities.values()) == pytest.approx(1.0)


@pytest.mark.parametrize("probability", [0.0, 1.0, -0.1, 1.1])
def test_career_probabilities_reject_invalid_value(probability: float):
    with pytest.raises(ValueError):
        career_probabilities(probability)


def test_career_odds_include_configured_overround():
    odds = career_odds(stay_probability=0.6, margin=0.05)

    assert sum(1.0 / value for value in odds.values()) == pytest.approx(1.05)


def test_summarize_book_updates_expected_and_worst_case_pnl():
    probabilities = career_probabilities(0.6)
    odds = career_odds(stay_probability=0.6, margin=0.05)
    bet = Bet("B1", "career", Outcome.HOME, 25.0, odds[Outcome.HOME])
    book = RiskBook.empty([Outcome.HOME, Outcome.AWAY])
    book.add_bet(bet)

    summary = summarize_book(book, [bet], probabilities)

    assert summary.bet_count == 1
    assert summary.total_stakes == pytest.approx(25.0)
    assert summary.expected_pnl == pytest.approx(1.19047619)
    assert summary.expected_roi == pytest.approx(0.04761905)
    assert summary.worst_case_pnl == pytest.approx(-14.68253968)


def test_summarize_empty_book_is_zero():
    book = RiskBook.empty([Outcome.HOME, Outcome.AWAY])

    summary = summarize_book(book, [], career_probabilities(0.6))

    assert summary.total_stakes == 0.0
    assert summary.expected_pnl == 0.0
    assert summary.expected_roi == 0.0
    assert summary.worst_case_pnl == 0.0


def test_settlement_rows_show_player_and_bookie_as_opposites():
    bets = [
        Bet("B1", "career", Outcome.HOME, 10.0, 2.0),
        Bet("B2", "career", Outcome.AWAY, 5.0, 3.0),
    ]

    bookie_total, rows = settlement_rows(bets, Outcome.HOME)

    assert bookie_total == pytest.approx(-5.0)
    assert rows[0]["Auszahlung"] == pytest.approx(20.0)
    assert rows[1]["Auszahlung"] == 0.0
    assert sum(float(row["Spieler-PnL"]) for row in rows) == pytest.approx(
        -bookie_total
    )

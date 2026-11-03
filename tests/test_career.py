import pytest

from bookie.career import career_odds, career_probabilities, settlement_rows
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

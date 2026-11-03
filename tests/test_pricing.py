import pytest

from bookie.engine.pricing import apply_margin, probs_to_odds
from bookie.engine.types import Outcome


def _fair_probs():
    # simple market with probabilities that sum to 1
    return {
        Outcome.HOME: 0.5,
        Outcome.DRAW: 0.3,
        Outcome.AWAY: 0.2,
    }


def test_apply_margin_sums_to_one_plus_margin():
    fair = _fair_probs()
    margin = 0.06

    implied = apply_margin(fair, margin)

    total_implied = sum(implied.values())
    # implied probabilities should sum to (1 + margin) up to numerical noise
    assert total_implied == pytest.approx(1.0 + margin, rel=1e-6, abs=1e-6)


def test_apply_margin_preserves_relative_weights():
    fair = _fair_probs()
    margin = 0.08

    implied = apply_margin(fair, margin)

    # Ratios of probabilities should be unchanged (pure scaling)
    ratio_fair_home_draw = fair[Outcome.HOME] / fair[Outcome.DRAW]
    ratio_implied_home_draw = implied[Outcome.HOME] / implied[Outcome.DRAW]

    assert ratio_implied_home_draw == pytest.approx(
        ratio_fair_home_draw, rel=1e-6, abs=1e-6
    )


def test_probs_to_odds_inverse_relationship_and_monotonicity():
    fair = _fair_probs()
    margin = 0.05

    implied = apply_margin(fair, margin)
    odds = probs_to_odds(implied)

    # Higher implied probability -> lower odds (monotonic)
    assert odds[Outcome.HOME] < odds[Outcome.DRAW]
    assert odds[Outcome.DRAW] < odds[Outcome.AWAY]

    # 1 / odds should approximately recover implied probabilities
    for outcome, p in implied.items():
        inv = 1.0 / odds[outcome]
        assert inv == pytest.approx(p, rel=1e-3, abs=1e-3)


def test_pricing_pipe_overround_matches_margin():
    fair = _fair_probs()
    margin = 0.07

    implied = apply_margin(fair, margin)
    odds = probs_to_odds(implied)

    overround = sum(1.0 / o for o in odds.values())
    # Overround (sum of implied probabilities from odds) should be ~ 1 + margin
    assert overround == pytest.approx(1.0 + margin, rel=1e-3, abs=1e-3)

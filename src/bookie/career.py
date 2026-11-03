"""Small domain adapter for the two-outcome career demo market."""

import random
from dataclasses import dataclass

from bookie.engine.pricing import apply_margin, probs_to_odds
from bookie.engine.risk import RiskBook
from bookie.engine.settlement import settle
from bookie.engine.types import Bet, Outcome

CAREER_OUTCOMES = (Outcome.HOME, Outcome.AWAY)
CAREER_LABELS = {
    Outcome.HOME: "Verbleib in der Firma",
    Outcome.AWAY: "Wechsel aus der Firma",
}
CAREER_MARKET_ID = "career-stay-or-leave"


@dataclass(frozen=True)
class BookSummary:
    """Probability-weighted and worst-case view of the current book."""

    bet_count: int
    total_stakes: float
    expected_pnl: float
    expected_roi: float
    worst_case_pnl: float


def career_probabilities(stay_probability: float) -> dict[Outcome, float]:
    """Build a binary probability surface from the probability of staying."""
    if not 0.0 < stay_probability < 1.0:
        raise ValueError("stay_probability must be strictly between 0 and 1")
    return {
        Outcome.HOME: stay_probability,
        Outcome.AWAY: 1.0 - stay_probability,
    }


def career_odds(stay_probability: float, margin: float) -> dict[Outcome, float]:
    """Quote decimal odds for the binary career market."""
    if not 0.0 <= margin <= 0.10:
        raise ValueError("margin must be between 0 and 0.10")
    fair = career_probabilities(stay_probability)
    return probs_to_odds(apply_margin(fair, margin))


def simulate_bet_request(
    request_number: int,
    probabilities: dict[Outcome, float],
    odds: dict[Outcome, float],
    seed: int,
) -> Bet:
    """Create one deterministic simulated bet request for the live dashboard."""
    if request_number < 1:
        raise ValueError("request_number must be positive")
    rng = random.Random(seed + request_number)
    outcome = (
        Outcome.HOME if rng.random() < probabilities[Outcome.HOME] else Outcome.AWAY
    )
    stake = float(rng.choice([5, 10, 25, 50]))
    return Bet(
        bet_id=f"S{request_number:03d}",
        market_id=CAREER_MARKET_ID,
        outcome=outcome,
        stake=stake,
        odds=odds[outcome],
    )


def summarize_book(
    book: RiskBook,
    bets: list[Bet],
    probabilities: dict[Outcome, float],
) -> BookSummary:
    """Summarize the live book using the configured fair probabilities."""
    scenario_pnl = book.worst_case_pnl()
    expected_pnl = sum(
        probabilities[outcome] * scenario_pnl[outcome] for outcome in CAREER_OUTCOMES
    )
    total_stakes = sum(book.stakes.values())
    expected_roi = expected_pnl / total_stakes if total_stakes else 0.0
    return BookSummary(
        bet_count=len(bets),
        total_stakes=total_stakes,
        expected_pnl=expected_pnl,
        expected_roi=expected_roi,
        worst_case_pnl=min(scenario_pnl.values()),
    )


def settlement_rows(
    bets: list[Bet], result: Outcome
) -> tuple[float, list[dict[str, str | float]]]:
    """Return bookmaker total and presentation-ready per-bet settlement rows."""
    total, per_bet = settle(bets, result)
    bookie_pnl_by_id = dict(per_bet)
    rows = []
    for bet in bets:
        won = bet.outcome == result
        bookie_pnl = bookie_pnl_by_id[bet.bet_id]
        rows.append(
            {
                "Wette": bet.bet_id,
                "Position": CAREER_LABELS[bet.outcome],
                "Einsatz": bet.stake,
                "Quote": bet.odds,
                "Auszahlung": bet.stake * bet.odds if won else 0.0,
                "Spieler-PnL": -bookie_pnl,
                "Bookie-PnL": bookie_pnl,
            }
        )
    return total, rows

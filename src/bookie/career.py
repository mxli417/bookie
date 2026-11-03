"""Small domain adapter for the two-outcome career demo market."""

from bookie.engine.pricing import apply_margin, probs_to_odds
from bookie.engine.settlement import settle
from bookie.engine.types import Bet, Outcome

CAREER_OUTCOMES = (Outcome.HOME, Outcome.AWAY)
CAREER_LABELS = {
    Outcome.HOME: "Verbleib in der Firma",
    Outcome.AWAY: "Wechsel aus der Firma",
}


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

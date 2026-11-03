"""
Simple "pricing" engine constructing odds with overround margins
(bookmaker margin odds).
"""

from typing import Dict

from bookie.engine.types import Outcome


def apply_margin(probs: Dict[Outcome, float], margin: float) -> Dict[Outcome, float]:
    """
    probs sum to 1.0 (fair)
    returns implied probs that sum to (1 + margin)
    """
    s = sum(probs.values())
    if s <= 0:
        raise ValueError("Probability sum must be > 0")
    # normalize first to sum 1
    norm = {k: v / s for k, v in probs.items()}
    # scale to overround
    return {k: v * (1.0 + margin) for k, v in norm.items()}


def probs_to_odds(
    implied_probs: Dict[Outcome, float], min_odds: float = 1.01
) -> Dict[Outcome, float]:
    odds = {}
    for k, p in implied_probs.items():
        if p <= 0:
            raise ValueError("Probability must be > 0")
        o = 1.0 / p
        odds[k] = max(min_odds, o)
    return odds

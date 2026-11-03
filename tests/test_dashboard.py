import pytest

from bookie.career import CAREER_OUTCOMES, career_odds, career_probabilities
from bookie.dashboard import (
    exposure_figure,
    liability_figure,
    pnl_figure,
    pricing_figure,
)
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome


@pytest.fixture
def populated_book() -> RiskBook:
    book = RiskBook.empty(CAREER_OUTCOMES)
    book.add_bet(Bet("B1", "career", Outcome.HOME, 25.0, 1.6))
    return book


def test_pricing_figure_compares_fair_and_offered_odds():
    probabilities = career_probabilities(0.6)
    figure = pricing_figure(probabilities, career_odds(0.6, 0.05))

    assert [trace.name for trace in figure.data] == ["Fair Odds", "Offered Odds"]
    assert list(figure.data[0].y) == pytest.approx([1 / 0.6, 1 / 0.4])


def test_risk_figures_use_current_book(populated_book: RiskBook):
    liability = liability_figure(populated_book)
    pnl = pnl_figure(populated_book, risk_floor=-200.0)

    assert list(liability.data[0].y) == pytest.approx([15.0, 0.0])
    assert list(pnl.data[0].y) == pytest.approx([-15.0, 25.0])
    assert pnl.layout.shapes[0].y0 == pytest.approx(-200.0)


def test_exposure_figure_handles_empty_and_populated_books(
    populated_book: RiskBook,
):
    assert exposure_figure(RiskBook.empty(CAREER_OUTCOMES)) is None

    exposure = exposure_figure(populated_book)

    assert exposure is not None
    assert list(exposure.data[0].values) == pytest.approx([25.0, 0.0])

"""Plotly figures for the Streamlit trading-style dashboard."""

import plotly.graph_objects as go

from bookie.career import CAREER_LABELS, CAREER_OUTCOMES
from bookie.engine.risk import RiskBook
from bookie.engine.types import Outcome

GREEN = "#00D084"
RED = "#FF5C5C"
BLUE = "#60A5FA"
AMBER = "#F5B942"
GRID = "rgba(148, 163, 184, 0.18)"


def _style(figure: go.Figure, title: str) -> go.Figure:
    figure.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=24, r=24, t=56, b=24),
        height=330,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hoverlabel=dict(namelength=-1),
    )
    figure.update_xaxes(gridcolor=GRID)
    figure.update_yaxes(gridcolor=GRID, zerolinecolor="rgba(148, 163, 184, 0.4)")
    return figure


def pricing_figure(
    probabilities: dict[Outcome, float], offered_odds: dict[Outcome, float]
) -> go.Figure:
    """Compare fair decimal odds with the currently offered prices."""
    labels = [CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES]
    fair_odds = [1.0 / probabilities[outcome] for outcome in CAREER_OUTCOMES]
    figure = go.Figure(
        data=[
            go.Bar(name="Fair Odds", x=labels, y=fair_odds, marker_color=BLUE),
            go.Bar(
                name="Offered Odds",
                x=labels,
                y=[offered_odds[outcome] for outcome in CAREER_OUTCOMES],
                marker_color=GREEN,
            ),
        ]
    )
    figure.update_layout(barmode="group")
    figure.update_yaxes(title_text="Dezimalquote")
    return _style(figure, "Pricing: Fair vs. Offered")


def liability_figure(book: RiskBook) -> go.Figure:
    """Show net bookmaker liability for each outcome."""
    figure = go.Figure(
        go.Bar(
            x=[CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES],
            y=[book.liability[outcome] for outcome in CAREER_OUTCOMES],
            marker_color=AMBER,
            name="Liability",
            text=[f"{book.liability[outcome]:.2f}" for outcome in CAREER_OUTCOMES],
            textposition="auto",
        )
    )
    figure.update_yaxes(title_text="Points")
    return _style(figure, "Net Liability by Outcome")


def pnl_figure(book: RiskBook, risk_floor: float) -> go.Figure:
    """Show outcome-conditioned bookmaker PnL and the configured risk floor."""
    pnl = book.worst_case_pnl()
    values = [pnl[outcome] for outcome in CAREER_OUTCOMES]
    figure = go.Figure(
        go.Bar(
            x=[CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES],
            y=values,
            marker_color=[GREEN if value >= 0 else RED for value in values],
            name="Bookmaker PnL",
            text=[f"{value:.2f}" for value in values],
            textposition="auto",
        )
    )
    figure.add_hline(
        y=risk_floor,
        line_dash="dash",
        line_color=RED,
        annotation_text=f"Risk Floor {risk_floor:.0f}",
        annotation_position="bottom right",
    )
    figure.update_yaxes(title_text="PnL in points")
    return _style(figure, "Outcome-conditioned Bookmaker PnL")


def exposure_figure(book: RiskBook) -> go.Figure | None:
    """Show accepted stake distribution, or no chart for an empty book."""
    values = [book.stakes[outcome] for outcome in CAREER_OUTCOMES]
    if not sum(values):
        return None
    figure = go.Figure(
        go.Pie(
            labels=[CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES],
            values=values,
            hole=0.64,
            marker=dict(colors=[BLUE, AMBER]),
            textinfo="label+percent",
            hovertemplate=(
                "%{label}<br>%{value:.2f} points<br>%{percent}<extra></extra>"
            ),
        )
    )
    figure.update_layout(showlegend=False)
    return _style(figure, "Stake Exposure Distribution")

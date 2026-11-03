"""Streamlit UI for the private career prediction market demo."""

import random

import streamlit as st

from bookie.career import (
    CAREER_LABELS,
    CAREER_OUTCOMES,
    career_odds,
    career_probabilities,
    settlement_rows,
    summarize_book,
)
from bookie.engine.accept import check_bet
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome

MARKET_ID = "career-stay-or-leave"


def _initialize_state() -> None:
    if "book" not in st.session_state:
        st.session_state.book = RiskBook.empty(CAREER_OUTCOMES)
        st.session_state.bets = []
        st.session_state.result = None
        st.session_state.simulation_index = 0


def _reset_market() -> None:
    for key in ("book", "bets", "result", "simulation_index"):
        st.session_state.pop(key, None)


def _money(value: float) -> str:
    return f"{value:,.2f} Punkte"


def main() -> None:
    st.set_page_config(
        page_title="Career Market Lab",
        page_icon="🎲",
        layout="wide",
    )
    _initialize_state()

    st.title("Career Market Lab")
    st.caption(
        "Privates Prognose-Experiment: Verbleib oder Wechsel — ausschließlich "
        "mit fiktiven Punkten."
    )
    with st.expander("Was bedeuten die Punkte?", expanded=True):
        st.markdown(
            "**Ein Punkt ist eine frei gewählte Recheneinheit, kein Euro und "
            "kein Kontoguthaben.** Du kannst zum Beispiel 100 Punkte gedanklich "
            "als dein Testbudget behandeln; die App erzwingt dieses Budget aber "
            "nicht. Der Einsatz ist die riskierte Menge. Eine Auszahlung enthält "
            "bei einer gewonnenen Wette Einsatz plus Gewinn. PnL bezeichnet nur "
            "den Nettogewinn oder -verlust — Spieler- und Bookie-PnL sind daher "
            "exakt gegensätzlich."
        )

    with st.sidebar:
        st.header("Marktparameter")
        stay_probability_percent = st.slider(
            "Faire Wahrscheinlichkeit für Verbleib",
            min_value=10,
            max_value=90,
            value=60,
            step=5,
            format="%d%%",
        )
        margin_percent = st.slider(
            "Bookie-Marge",
            min_value=0,
            max_value=10,
            value=5,
            step=1,
            format="%d%%",
        )
        risk_floor = st.number_input(
            "Minimaler Worst-Case-PnL",
            min_value=-10_000.0,
            max_value=0.0,
            value=-200.0,
            step=10.0,
        )
        seed = st.number_input("Simulations-Seed", min_value=0, value=42, step=1)
        if st.button("Markt zurücksetzen", width="stretch"):
            _reset_market()
            st.rerun()

    stay_probability = stay_probability_percent / 100.0
    margin = margin_percent / 100.0
    odds = career_odds(stay_probability, margin)
    probabilities = career_probabilities(stay_probability)

    quote_columns = st.columns(2)
    for column, outcome in zip(quote_columns, CAREER_OUTCOMES, strict=True):
        column.metric(CAREER_LABELS[outcome], f"{odds[outcome]:.2f}")

    st.subheader("Wette platzieren")
    if st.session_state.result is not None:
        st.info("Dieser Markt ist abgerechnet. Setze ihn für eine neue Runde zurück.")

    with st.form("bet_form", clear_on_submit=False):
        selected_label = st.radio(
            "Position",
            [CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES],
            horizontal=True,
        )
        stake = st.number_input(
            "Einsatz in Spielpunkten",
            min_value=1.0,
            max_value=10_000.0,
            value=25.0,
            step=5.0,
            help=(
                "Fiktive Recheneinheiten, die du auf dieses Outcome setzt. "
                "Es gibt kein echtes Guthaben und keine Zahlung."
            ),
        )
        submitted = st.form_submit_button(
            "Wette anfragen",
            disabled=st.session_state.result is not None,
            width="stretch",
        )

    if submitted:
        outcome = next(
            key for key, label in CAREER_LABELS.items() if label == selected_label
        )
        bet = Bet(
            bet_id=f"B{len(st.session_state.bets) + 1}",
            market_id=MARKET_ID,
            outcome=outcome,
            stake=float(stake),
            odds=odds[outcome],
        )
        decision = check_bet(st.session_state.book, bet, risk_floor)
        if decision.accepted:
            st.session_state.book.add_bet(bet)
            st.session_state.bets.append(bet)
            st.success(f"{bet.bet_id} angenommen — Quote {bet.odds:.2f}")
        else:
            st.error(f"Wette abgelehnt: {decision.reason}")

    st.subheader("Live-Bookie-Bilanz")
    pnl = st.session_state.book.worst_case_pnl()
    summary = summarize_book(
        st.session_state.book, st.session_state.bets, probabilities
    )
    st.caption(
        "Wird nach jeder angenommenen Wette aktualisiert. Der erwartete PnL "
        "gewichtet beide möglichen Bookie-Ergebnisse mit den links eingestellten "
        "fairen Wahrscheinlichkeiten."
    )
    summary_columns = st.columns(4)
    summary_columns[0].metric("Angenommene Wetten", summary.bet_count)
    summary_columns[1].metric("Einsatzvolumen", _money(summary.total_stakes))
    summary_columns[2].metric(
        "Erwarteter Bookie-PnL",
        _money(summary.expected_pnl),
        delta=(
            f"{summary.expected_roi:.1%} vom Einsatzvolumen"
            if summary.total_stakes
            else None
        ),
    )
    summary_columns[3].metric("Worst-Case-PnL", _money(summary.worst_case_pnl))

    st.markdown("**Bookie-PnL je möglichem Outcome**")
    outcome_columns = st.columns(2)
    outcome_columns[0].metric("Bei Verbleib", _money(pnl[Outcome.HOME]))
    outcome_columns[1].metric("Bei Wechsel", _money(pnl[Outcome.AWAY]))
    st.dataframe(
        [
            {
                "Outcome": CAREER_LABELS[outcome],
                "Bookie-PnL": pnl[outcome],
            }
            for outcome in CAREER_OUTCOMES
        ],
        width="stretch",
        hide_index=True,
    )

    if st.session_state.bets:
        st.dataframe(
            [
                {
                    "Wette": bet.bet_id,
                    "Position": CAREER_LABELS[bet.outcome],
                    "Einsatz": bet.stake,
                    "Quote": round(bet.odds, 2),
                }
                for bet in st.session_state.bets
            ],
            width="stretch",
            hide_index=True,
        )
    else:
        st.caption("Noch keine Wette angenommen.")

    st.subheader("Outcome simulieren und abrechnen")
    if st.button(
        "Outcome simulieren",
        disabled=not st.session_state.bets or st.session_state.result is not None,
        type="primary",
        width="stretch",
    ):
        rng = random.Random(int(seed) + st.session_state.simulation_index)
        st.session_state.simulation_index += 1
        st.session_state.result = (
            Outcome.HOME if rng.random() < probabilities[Outcome.HOME] else Outcome.AWAY
        )

    if st.session_state.result is not None:
        result = st.session_state.result
        bookie_total, rows = settlement_rows(st.session_state.bets, result)
        st.success(f"Simuliertes Ergebnis: {CAREER_LABELS[result]}")
        settlement_columns = st.columns(3)
        settlement_columns[0].metric("Bookie-PnL", _money(bookie_total))
        settlement_columns[1].metric("Spieler-PnL", _money(-bookie_total))
        settlement_columns[2].metric(
            "Spielerauszahlung",
            _money(sum(float(row["Auszahlung"]) for row in rows)),
        )
        st.dataframe(rows, width="stretch", hide_index=True)

    st.divider()
    st.caption(
        "Keine Echtgeldfunktion, keine Konten, keine Zahlungen und keine "
        "Vorhersageberatung."
    )


if __name__ == "__main__":
    main()

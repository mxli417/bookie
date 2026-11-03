"""Streamlit UI for the private career prediction market demo."""

import random

import streamlit as st

from bookie.career import (
    CAREER_LABELS,
    CAREER_MARKET_ID,
    CAREER_OUTCOMES,
    career_odds,
    career_probabilities,
    settlement_rows,
    simulate_bet_request,
    summarize_book,
)
from bookie.dashboard import (
    exposure_figure,
    liability_figure,
    pnl_figure,
    pricing_figure,
)
from bookie.engine.accept import check_bet
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome


def _initialize_state() -> None:
    if "book" not in st.session_state:
        st.session_state.book = RiskBook.empty(CAREER_OUTCOMES)
        st.session_state.bets = []
        st.session_state.result = None
        st.session_state.simulation_index = 0
        st.session_state.request_count = 0
        st.session_state.decision_log = []


def _reset_market() -> None:
    for key in (
        "book",
        "bets",
        "result",
        "simulation_index",
        "request_count",
        "decision_log",
    ):
        st.session_state.pop(key, None)


def _money(value: float) -> str:
    return f"{value:,.2f} points"


def _process_bet(bet: Bet, risk_floor: float) -> bool:
    decision = check_bet(st.session_state.book, bet, risk_floor)
    if decision.accepted:
        st.session_state.book.add_bet(bet)
        st.session_state.bets.append(bet)
    st.session_state.decision_log.insert(
        0,
        {
            "Request": bet.bet_id,
            "Decision": "ACCEPTED" if decision.accepted else "REJECTED",
            "Outcome": CAREER_LABELS[bet.outcome],
            "Stake": bet.stake,
            "Odds": round(bet.odds, 2),
            "Projected worst case": round(decision.projected_worst_case_pnl, 2),
            "Risk floor": round(decision.risk_floor, 2),
            "Reason": decision.reason,
        },
    )
    return decision.accepted


def main() -> None:
    st.set_page_config(
        page_title="Career Market Lab",
        page_icon="🎲",
        layout="wide",
    )
    _initialize_state()

    st.title("Career Market Lab")
    st.caption(
        "Private prediction experiment: stay or leave — using fictional "
        "play points only."
    )
    with st.expander("What do the points mean?", expanded=True):
        st.markdown(
            "**A point is an arbitrary accounting unit, not a euro and not an "
            "account balance.** You may think of 100 points as a test bankroll, "
            "but the app does not enforce that bankroll. The stake is the amount "
            "at risk. A winning payout includes the returned stake plus profit. "
            "PnL is net profit or loss, so player and bookmaker PnL are exact "
            "opposites."
        )

    with st.sidebar:
        st.header("Market Parameters")
        stay_probability_percent = st.slider(
            "Fair probability of staying",
            min_value=10,
            max_value=90,
            value=60,
            step=5,
            format="%d%%",
        )
        margin_percent = st.slider(
            "Bookmaker margin",
            min_value=0,
            max_value=10,
            value=5,
            step=1,
            format="%d%%",
        )
        risk_floor = st.number_input(
            "Minimum worst-case PnL",
            min_value=-10_000.0,
            max_value=0.0,
            value=-200.0,
            step=10.0,
        )
        seed = st.number_input("Simulation seed", min_value=0, value=42, step=1)
        if st.button("Reset market", width="stretch"):
            _reset_market()
            st.rerun()

    stay_probability = stay_probability_percent / 100.0
    margin = margin_percent / 100.0
    odds = career_odds(stay_probability, margin)
    probabilities = career_probabilities(stay_probability)

    st.subheader("Market Pricing")
    quote_columns = st.columns(2)
    for column, outcome in zip(quote_columns, CAREER_OUTCOMES, strict=True):
        fair_odds = 1.0 / probabilities[outcome]
        column.metric(
            CAREER_LABELS[outcome],
            f"{odds[outcome]:.2f}",
            delta=f"Fair {fair_odds:.2f}",
            delta_color="off",
        )
    st.plotly_chart(
        pricing_figure(probabilities, odds),
        width="stretch",
        config={"displayModeBar": False},
    )

    st.subheader("Order Entry & Simulation")
    if st.session_state.result is not None:
        st.info("This market is settled. Reset it to start a new round.")

    entry_column, simulator_column = st.columns([3, 2])
    with entry_column:
        with st.form("bet_form", clear_on_submit=False):
            selected_label = st.radio(
                "Position",
                [CAREER_LABELS[outcome] for outcome in CAREER_OUTCOMES],
                horizontal=True,
            )
            stake = st.number_input(
                "Stake in play points",
                min_value=1.0,
                max_value=10_000.0,
                value=25.0,
                step=5.0,
                help=(
                    "Fictional accounting units staked on this outcome. "
                    "There is no real balance or payment."
                ),
            )
            submitted = st.form_submit_button(
                "Submit bet request",
                disabled=st.session_state.result is not None,
                width="stretch",
            )
    with simulator_column:
        st.markdown("**Deterministic order flow**")
        st.caption(
            "Generates one reproducible bet request. Outcome and stake follow "
            "the seed, market probability, and a fixed stake set."
        )
        simulated = st.button(
            "Simulate next bet request",
            disabled=st.session_state.result is not None,
            width="stretch",
        )

    if submitted:
        st.session_state.request_count += 1
        outcome = next(
            key for key, label in CAREER_LABELS.items() if label == selected_label
        )
        bet = Bet(
            bet_id=f"M{st.session_state.request_count:03d}",
            market_id=CAREER_MARKET_ID,
            outcome=outcome,
            stake=float(stake),
            odds=odds[outcome],
        )
        if _process_bet(bet, risk_floor):
            st.success(f"{bet.bet_id} accepted — odds {bet.odds:.2f}")
        else:
            st.error(
                f"{bet.bet_id} rejected: "
                f"{st.session_state.decision_log[0]['Reason']}"
            )

    if simulated:
        st.session_state.request_count += 1
        bet = simulate_bet_request(
            st.session_state.request_count,
            probabilities,
            odds,
            int(seed),
        )
        if _process_bet(bet, risk_floor):
            st.success(
                f"{bet.bet_id} simulated and accepted — "
                f"{CAREER_LABELS[bet.outcome]}, {bet.stake:.0f} points"
            )
        else:
            st.warning(
                f"{bet.bet_id} simulated and rejected — "
                f"{st.session_state.decision_log[0]['Reason']}"
            )

    st.subheader("Live Bookmaker Position")
    with st.expander("How to read PnL", expanded=True):
        st.markdown(
            "**PnL means profit and loss from the bookmaker's perspective.**\n\n"
            "- A **positive** PnL is bookmaker profit; a **negative** PnL is "
            "bookmaker loss.\n"
            "- **Expected bookmaker PnL** is the probability-weighted average "
            "before settlement. It is an estimate, not a guaranteed profit.\n"
            "- **Outcome PnL** is what the bookmaker realizes if that specific "
            "outcome occurs.\n"
            "- **Worst-case PnL** is the lowest outcome PnL currently in the "
            "book. A new bet is accepted only when its projected worst case "
            "stays at or above the risk floor."
        )
    pnl = st.session_state.book.worst_case_pnl()
    summary = summarize_book(
        st.session_state.book, st.session_state.bets, probabilities
    )
    st.caption(
        "Updated after every accepted bet. Expected PnL weights both possible "
        "bookmaker results using the fair probabilities configured on the left."
    )
    rejected_count = sum(
        row["Decision"] == "REJECTED" for row in st.session_state.decision_log
    )
    summary_columns = st.columns(5)
    summary_columns[0].metric("Accepted bets", summary.bet_count)
    summary_columns[1].metric("Rejected bets", rejected_count)
    summary_columns[2].metric("Stake volume", _money(summary.total_stakes))
    summary_columns[3].metric(
        "Expected bookmaker PnL",
        _money(summary.expected_pnl),
        delta=(
            f"{summary.expected_roi:.1%} of stake volume"
            if summary.total_stakes
            else None
        ),
    )
    summary_columns[4].metric("Worst-case PnL", _money(summary.worst_case_pnl))

    if not summary.total_stakes:
        st.info("Expected bookmaker edge appears after the first accepted bet.")
    elif summary.expected_pnl > 0:
        st.success(
            "POSITIVE EXPECTED BOOKMAKER EDGE: "
            f"+{_money(summary.expected_pnl)} "
            f"({summary.expected_roi:.1%} of accepted stakes). "
            "This is an expectation, not realized profit."
        )
    elif summary.expected_pnl < 0:
        st.error(
            "NEGATIVE EXPECTED BOOKMAKER EDGE: "
            f"{_money(summary.expected_pnl)} "
            f"({summary.expected_roi:.1%} of accepted stakes)."
        )
    else:
        st.warning("Expected bookmaker PnL is currently break-even at 0.00 points.")

    st.markdown("**Bookmaker PnL by possible outcome**")
    outcome_columns = st.columns(2)
    outcome_columns[0].metric("If staying", _money(pnl[Outcome.HOME]))
    outcome_columns[1].metric("If leaving", _money(pnl[Outcome.AWAY]))
    pnl_column, liability_column = st.columns(2)
    pnl_column.plotly_chart(
        pnl_figure(st.session_state.book, risk_floor),
        width="stretch",
        config={"displayModeBar": False},
    )
    liability_column.plotly_chart(
        liability_figure(st.session_state.book),
        width="stretch",
        config={"displayModeBar": False},
    )

    exposure_column, decisions_column = st.columns(2)
    with exposure_column:
        exposure_chart = exposure_figure(st.session_state.book)
        if exposure_chart is None:
            st.info("Exposure appears after the first accepted bet.")
        else:
            st.plotly_chart(
                exposure_chart,
                width="stretch",
                config={"displayModeBar": False},
            )
    with decisions_column:
        st.markdown("**Acceptance / Rejection Feed**")
        if st.session_state.decision_log:
            st.dataframe(
                st.session_state.decision_log,
                width="stretch",
                hide_index=True,
            )
        else:
            st.info("No bet request has been evaluated yet.")

    if st.session_state.bets:
        st.dataframe(
            [
                {
                    "Bet": bet.bet_id,
                    "Position": CAREER_LABELS[bet.outcome],
                    "Stake": bet.stake,
                    "Odds": round(bet.odds, 2),
                }
                for bet in st.session_state.bets
            ],
            width="stretch",
            hide_index=True,
        )
    else:
        st.caption("No bet has been accepted yet.")

    st.subheader("Simulate Outcome & Settle")
    if st.button(
        "Simulate outcome",
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
        st.info(f"Simulated result: {CAREER_LABELS[result]}")
        if bookie_total > 0:
            st.success(f"BOOKMAKER PROFIT: +{_money(bookie_total)}")
        elif bookie_total < 0:
            st.error(f"BOOKMAKER LOSS: {_money(bookie_total)}")
        else:
            st.warning("BOOKMAKER RESULT: break-even at 0.00 points")
        settlement_columns = st.columns(3)
        settlement_columns[0].metric("Realized bookmaker PnL", _money(bookie_total))
        settlement_columns[1].metric("Player PnL", _money(-bookie_total))
        settlement_columns[2].metric(
            "Player payout",
            _money(sum(float(row["Payout"]) for row in rows)),
        )
        st.dataframe(rows, width="stretch", hide_index=True)

    st.divider()
    st.caption("No real-money functionality, accounts, payments, or prediction advice.")


if __name__ == "__main__":
    main()

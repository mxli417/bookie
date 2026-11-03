from pathlib import Path

from streamlit.testing.v1 import AppTest

WEB_APP = Path(__file__).parents[1] / "src" / "bookie" / "web.py"


def _metric_value(app: AppTest, label: str) -> str:
    return next(metric.value for metric in app.metric if metric.label == label)


def _button(app: AppTest, label: str):
    return next(button for button in app.button if button.label == label)


def _number_input(app: AppTest, label: str):
    return next(widget for widget in app.number_input if widget.label == label)


def test_streamlit_happy_path_accepts_and_settles_bet():
    app = AppTest.from_file(WEB_APP).run(timeout=10)

    assert not app.exception
    assert app.title[0].value == "Career Market Lab"
    assert _metric_value(app, "Accepted bets") == "0"
    assert _metric_value(app, "Stake volume") == "0.00 points"

    _button(app, "Submit bet request").click().run(timeout=10)

    assert not app.exception
    assert _metric_value(app, "Accepted bets") == "1"
    assert _metric_value(app, "Stake volume") == "25.00 points"
    assert _metric_value(app, "Expected bookmaker PnL") == "1.19 points"
    assert _metric_value(app, "Worst-case PnL") == "-14.68 points"
    assert app.success[0].value.startswith("M001 accepted")
    assert any(
        message.value.startswith("POSITIVE EXPECTED BOOKMAKER EDGE: +1.19 points")
        for message in app.success
    )

    _button(app, "Simulate outcome").click().run(timeout=10)

    assert not app.exception
    metric_labels = [metric.label for metric in app.metric]
    assert "Realized bookmaker PnL" in metric_labels
    assert "Player PnL" in metric_labels
    assert "Player payout" in metric_labels
    assert any(
        message.value == "BOOKMAKER PROFIT: +25.00 points" for message in app.success
    )


def test_streamlit_shows_risk_rejection():
    app = AppTest.from_file(WEB_APP).run(timeout=10)
    _number_input(app, "Minimum worst-case PnL").set_value(0.0)

    _button(app, "Submit bet request").click().run(timeout=10)

    assert not app.exception
    assert _metric_value(app, "Accepted bets") == "0"
    assert _metric_value(app, "Rejected bets") == "1"
    assert app.error[0].value == (
        "M001 rejected: Projected worst-case PnL -14.68 " "breaches risk floor 0.00."
    )


def test_streamlit_simulated_request_updates_dashboard():
    app = AppTest.from_file(WEB_APP).run(timeout=10)

    _button(app, "Simulate next bet request").click().run(timeout=10)

    assert not app.exception
    assert _metric_value(app, "Accepted bets") == "1"
    assert _metric_value(app, "Stake volume") != "0.00 points"
    assert app.success[0].value.startswith("S001 simulated and accepted")

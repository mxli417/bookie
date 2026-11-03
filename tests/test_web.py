from pathlib import Path

from streamlit.testing.v1 import AppTest

WEB_APP = Path(__file__).parents[1] / "src" / "bookie" / "web.py"


def test_streamlit_happy_path_accepts_and_settles_bet():
    app = AppTest.from_file(WEB_APP).run(timeout=10)

    assert not app.exception
    assert app.title[0].value == "Career Market Lab"
    assert app.metric[2].value == "0"

    app.button[0].click().run(timeout=10)

    assert not app.exception
    assert app.metric[2].value == "1"
    assert app.success[0].value.startswith("B1 angenommen")

    app.button[1].click().run(timeout=10)

    assert not app.exception
    metric_labels = [metric.label for metric in app.metric]
    assert "Bookie-PnL" in metric_labels
    assert "Spieler-PnL" in metric_labels
    assert "Spielerauszahlung" in metric_labels


def test_streamlit_shows_risk_rejection():
    app = AppTest.from_file(WEB_APP).run(timeout=10)
    app.number_input[1].set_value(0.0)

    app.button[0].click().run(timeout=10)

    assert not app.exception
    assert app.metric[2].value == "0"
    assert app.error[0].value.startswith("Wette abgelehnt: RISK_LIMIT")

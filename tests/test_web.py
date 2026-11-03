from pathlib import Path

from streamlit.testing.v1 import AppTest

WEB_APP = Path(__file__).parents[1] / "src" / "bookie" / "web.py"


def _metric_value(app: AppTest, label: str) -> str:
    return next(metric.value for metric in app.metric if metric.label == label)


def test_streamlit_happy_path_accepts_and_settles_bet():
    app = AppTest.from_file(WEB_APP).run(timeout=10)

    assert not app.exception
    assert app.title[0].value == "Career Market Lab"
    assert _metric_value(app, "Angenommene Wetten") == "0"
    assert _metric_value(app, "Einsatzvolumen") == "0.00 Punkte"

    app.button[0].click().run(timeout=10)

    assert not app.exception
    assert _metric_value(app, "Angenommene Wetten") == "1"
    assert _metric_value(app, "Einsatzvolumen") == "25.00 Punkte"
    assert _metric_value(app, "Erwarteter Bookie-PnL") == "1.19 Punkte"
    assert _metric_value(app, "Worst-Case-PnL") == "-14.68 Punkte"
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
    assert _metric_value(app, "Angenommene Wetten") == "0"
    assert app.error[0].value.startswith("Wette abgelehnt: RISK_LIMIT")

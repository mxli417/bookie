# AGENTS.md

## Purpose and boundaries

Bookie is a private educational simulation for pricing and bookmaker-risk
research. Keep the mathematical engine transparent and deterministic. Do not
add payments, real-money wagering, customer accounts or deployment as a
gambling service.

## Environment

- Use Python 3.14 from the repository-local `.venv`.
- Install and lock dependencies with `uv`; keep `uv.lock` versioned.
- Run Python, pytest, Ruff, Black and application commands from `.venv`.
- Never commit `.venv`, `.uv-cache`, generated caches or local editor state.

## Architecture

- `src/bookie/engine` is the framework-independent domain core.
- UI and simulations may import the engine; the engine must not import them.
- `src/bookie/web.py` is a thin Streamlit UI; keep business rules out of it.
- `src/bookie/dashboard.py` owns Plotly presentation figures and no risk rules.
- Accepted odds are immutable and stored on each `Bet`.
- `RiskBook.worst_case_pnl()` is the source of truth for scenario exposure.
- `check_bet()` is a non-mutating preview. Callers explicitly add accepted bets.
- Settlement values are bookmaker PnL; player net PnL has the opposite sign.

## Change rules

- Add or update tests for every change to pricing, risk, acceptance or settlement.
- Include boundary cases and hand-checkable PnL examples.
- Keep public behavior typed and prefer pure functions in the engine.
- Validate with the commands below before committing.
- Keep the README roadmap intact unless the project direction actually changes.

## Required checks

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\black.exe --check src tests
```

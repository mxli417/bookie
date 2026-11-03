# Bookie — a tiny bookmaker risk & pricing engine

Bookie is a small research project for studying fixed-odds pricing, exposure,
liability and risk limits. It is an educational simulation, not a gambling
service or financial product.

## Implemented

- fixed-odds markets using explicit outcomes
- fair probabilities to implied probabilities and decimal odds
- configurable bookmaker margin (overround)
- stake and liability tracking per outcome
- outcome-conditioned and worst-case bookmaker PnL
- acceptance decisions based on a minimum worst-case PnL
- settlement with total and per-bet bookmaker PnL
- deterministic toy simulation from a random seed

The initial simulation uses a three-outcome 1X2 market (`HOME`, `DRAW`, `AWAY`).
The engine functions themselves stay deliberately small and deterministic.

## Architecture

```text
src/bookie/
  engine/
    types.py        # Market, Bet, Outcome and Price data types
    pricing.py      # probabilities -> overround -> decimal odds
    risk.py         # stakes, liability and scenario PnL
    accept.py       # hypothetical risk check before accepting a bet
    settlement.py   # realized bookmaker PnL
  sim/
    runner.py       # deterministic toy market simulation
  main.py           # console entry point
tests/              # unit tests for pricing, risk, acceptance and settlement
```

The dependency direction is `UI/simulation -> engine`. The engine has no UI,
database or framework dependency. A bet stores its accepted odds so later
price changes cannot alter its settlement.

For an outcome `i`, the bookmaker scenario PnL is:

```text
PnL(i) = stakes on all losing outcomes - liability on outcome i
```

The acceptance policy copies the current risk book, adds the candidate bet to
that copy and rejects it when the resulting minimum scenario PnL is below the
configured risk floor. The caller adds an accepted bet to the real book.

## Setup

The project uses Python 3.14 and [uv](https://docs.astral.sh/uv/). From the
repository root on Windows:

```powershell
py -3.14 -m venv .venv
$env:UV_CACHE_DIR = "$PWD\.uv-cache"
uv sync --extra dev
```

Run all commands through the repository environment:

```powershell
.\.venv\Scripts\bookie.exe
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\black.exe --check src tests
```

The dependency lock is stored in `uv.lock`. Regenerate it with `uv lock` only
after intentionally changing a dependency.

## Library example

```python
from bookie.engine.accept import check_bet
from bookie.engine.risk import RiskBook
from bookie.engine.types import Bet, Outcome

book = RiskBook.empty([Outcome.HOME, Outcome.AWAY])
bet = Bet("B1", "career", Outcome.HOME, stake=10.0, odds=1.9)
decision = check_bet(book, bet, min_worst_case_pnl=-100.0)
if decision.accepted:
    book.add_bet(bet)
```

## Current limitations

- in-memory state only
- one market at a time in the toy simulation
- no capital account or multi-market ruin process
- no authentication, payments or real-money handling
- fixed exogenous fair probabilities
- no correlated outcomes or combination bets

## Roadmap

- Monte-Carlo ruin simulations with policy comparisons
- extend calculations to a Rust/C++ core via `pyo3` / `pybind11`
- extend the engine to handle additional market types
- exposure-aware requoting
- optional Poisson and xG-based pricing models
- optional correlated outcomes and combination bets

## References

- Huygens, C. (1657), *De ratiociniis in ludo aleae*
- de Moivre, A. (1718/1756), *The Doctrine of Chances*

## Disclaimer

This repository is for educational and private research purposes only. It is
not a betting platform, gambling service or financial product. Do not use it
to take real-money bets.

# Bookie — a tiny bookmaker risk & pricing engine (mini-research project)

**Bookie** is a small, research-oriented bookmaker engine built to study:

* bookmaker odds, bets and risk handling
* probabilistic pricing (probabilities -> odds -> margin)
* exposure & liability tracking
* worst-case Profit-and-Loss (PnL) calculation and acceptance rules

It is not a gambling product — it is a **toy research engine** to explore how 
bookmakers combine probability models and risk constraints to avoid insolvency 
under uncertainty.

## Motivation

I am a statistician by trade and fascinated by stochastic modeling in real-world systems — especially where randomness, incentives, and risk interact.

Inspired by early probability texts such as Huygens’ *De Ratiociniis in Ludo Aleae* (1657) and de Moivre’s *The Doctrine of Chances* (1718/1756), this project uses simulated betting markets as a didactic platform for exploring modern risk and pricing structures in stochastic environments.

* how odds encode implied probabilities
* how margins generate positive expected value for the bookmaker
* why **risk management — not prediction — prevents ruin**

The engine is deliberately small, transparent, and mathematically explicit.

## What this engine does

This project implements a minimal **fixed-odds pre-match bookmaker core**:

1. **Pricing**: Convert fair probabilities into odds with overround (margin)

2. **Risk Tracking**: Track stakes & liability per outcome

3. **Worst-Case PnL**: Compute outcome-conditioned cashflow

4. **Bet Acceptance Policy**: Accept / reject bets based on risk limits

5. **Settlement**: Resolve bets and compute realized PnL

A small simulation harness demonstrates how:

* margins ≠ guaranteed safety
* a few extreme outcomes dominate risk
* acceptance limits stabilize worst-case exposure


## Project structure

```
bookie/
  engine/
    types.py        # Market, Bet, Outcome, Price
    pricing.py      # probs → implied probs → odds (with margin)
    risk.py         # stakes, liability, worst-case PnL - bookie core
    accept.py       # accept / reject logic
    settlement.py   # resolve bets & compute PnL
  sim/
    runner.py      # toy simulation of bettors & outcomes
  tests/
    test_pricing.py
    test_risk.py
```

Design principles:

* pure & deterministic core functions
* explicit data structures
* easy to test, reason about, and later port to Rust/C++ (optional extension)


## Why this project exists

This engine is a **tiny research laboratory** for questions like:

* How does margin translate into expected profit?
* Why can a bookmaker still go bankrupt?
* How do stake limits cap Pareto-style tail risk?
* What happens to ruin probability under different policies?

The project sits at the intersection of:

* applied probability
* stochastic processes
* actuarial risk theory
* simulation & systems modeling


## Current potential roadmap (evolved as time allows)

* Monte-Carlo ruin simulations with policy comparisons
* extend calculations to: Rust / C++ core via `pyo3` / `pybind11`
* extend the engine to handle multi-outcome bets
* dynamics: exposure-aware requoting
* optional: Poisson & xG-based pricing models
* optional: correlated outcomes & combo bets

## Disclaimer

This project is for **educational and private research purposes only**.
It is not a betting platform, gambling service, or financial product.

The goal is to study **risk, incentives, and stochastic structure** — the same spirit in which early probability theory was developed.

## References

- Huygens, C. (1657). De ratiociniis in ludo aleae [On reasoning in games of chance] (C. Doyle, Trans.). Dartmouth College Mathematics Department.
Retrieved from: https://math.dartmouth.edu/~doyle/docs/huygens/huygens.pdf

- de Moivre, A. (1718/1756). The Doctrine of Chances: or, A Method of Calculating the Probability of Events in Play (Reprint ed.). London: J. Tonson.
Retrieved from: https://archive.org/details/doctrineofchance00moiv
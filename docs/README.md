# Bookie Documentation

This documentation explains the project's domain model independently of the
Streamlit interface. All monetary values are fictional play points.

## Start here

1. [Pricing, overround, and bookmaker risk](pricing-and-risk.md) explains the
   path from fair probabilities to offered odds, distinguishes overround from
   realized profit, and documents the bet acceptance policy.
2. The project [README](../README.md) covers installation, commands,
   architecture, and the roadmap.
3. Executable examples are available in `src/bookie/sim/runner.py` and the
   local Streamlit application in `src/bookie/web.py`.

## Core idea

> A bookmaker does not need to know the next outcome. It needs to price the
> probability distribution reasonably well and maintain a book whose possible
> losses do not exceed its risk capacity.

That is not a guarantee of profit. Miscalibrated probabilities, one-sided
order flow, correlations, and rare extreme events remain real risks. The small
engine is designed to make this distinction between prediction and risk
management explicit.

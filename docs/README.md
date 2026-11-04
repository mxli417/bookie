# Bookie Documentation

This documentation explains the project's domain model independently of the
Streamlit interface. All monetary values are fictional play points.

## Start here

1. [When can every outcome be profitable?](book-balancing.md) gives the short
   mathematical explanation for a balanced, all-positive book.
2. [Pricing, overround, and bookmaker risk](pricing-and-risk.md) explains the
   path from fair probabilities to offered odds, distinguishes overround from
   realized profit, and documents the bet acceptance policy.
3. [Sources, evidence, and scope](sources.md) distinguishes introductory
   material from project derivations and academic evidence.
4. The project [README](../README.md) covers installation, commands,
   architecture, and the roadmap.
5. Executable examples are available in `src/bookie/sim/runner.py` and the
   local Streamlit application in `src/bookie/web.py`.

## Build the Sphinx site

Install the development dependencies with `uv sync --extra dev`, then run
from the repository root:

```powershell
.\.venv\Scripts\sphinx-build.exe -W -b html docs docs\_build\html
```

Open `docs\_build\html\index.html` locally. The generated `_build` directory
is ignored by Git.

## Core idea

> A bookmaker does not need to know the next outcome. It needs to price the
> probability distribution reasonably well and maintain a book whose possible
> losses do not exceed its risk capacity.

That is not a guarantee of profit. Miscalibrated probabilities, one-sided
order flow, correlations, and rare extreme events remain real risks. The small
engine is designed to make this distinction between prediction and risk
management explicit.

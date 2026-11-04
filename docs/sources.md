# Sources, evidence, and scope

This page separates introductory source material from the claims and
derivations that go beyond it. Bookie is an educational mathematical model,
not a description of every practice used by a real bookmaker.

## Baseline source

The requested starting point is the German Wikipedia article
[*Buchmacher*](https://de.wikipedia.org/wiki/Buchmacher). It provides a useful
introductory account of:

- bookmakers offering odds on future outcomes;
- accepted fixed-odds bets retaining the agreed price;
- stake limits, opposing bets, and price changes as possible risk controls;
- the bookmaker not necessarily needing to predict the winning outcome;
- reciprocal odds being used to calculate an implied payout rate.

Wikipedia is used here for orientation, not as the sole authority. The article
itself is flagged as lacking citations, and its description of a bookmaker
continually adjusting prices to obtain an ideal arbitrage position is a
simplification rather than a universal empirical result.[^wiki]

## Where Bookie goes beyond that baseline

| Topic | What is added beyond the introductory account | Basis |
| --- | --- | --- |
| Scenario accounting | The exact identity $\operatorname{PnL}(i)=S-G_i$ | Direct derivation from the engine's bookmaker-PnL convention |
| All-positive book | The necessary and sufficient condition $G_i<S$ for every outcome | Direct algebraic consequence of the scenario identity |
| Fixed-odds allocation | The equivalent condition $w_i<1/O_i$ and feasibility when $\sum_i 1/O_i>1$ | Project derivation; the overround definition is supported by Clarke et al.[^clarke] |
| Equal-PnL allocation | Under proportional margin and $w_i=p_i$, every outcome returns $S m/(1+m)$ | Project-specific derivation from Bookie's pricing rule |
| Expected return | The distinction between overround, expected loss, and realized profit | Hegarty and Whelan show the assumptions required for the conventional overround formula.[^hegarty] |
| Real-world behaviour | A balanced book is possible but is not necessarily the objective or observed state of each real market | Levitt and Franck et al. discuss prediction, bettor demand, price shading, and exposure.[^levitt] [^franck] |
| Locked prices | Later odds changes do not alter an already accepted fixed-odds claim | Wikipedia's overview and Franck et al.[^wiki] [^franck] |

The algebra in the first four rows is transparent model analysis rather than a
claim copied from an external source. It follows from Bookie's definitions and
can be checked against `RiskBook.worst_case_pnl()`.

## Interpretation limits

The exact balanced-book result is a possibility theorem: an overround creates
enough implied-probability capacity for a suitable stake allocation to be
profitable in every modeled outcome. It does **not** say that incoming stakes
will have that allocation, that a real bookmaker can always reach it, or that
overround equals realized profit.

Research provides good reasons to keep those ideas separate. Levitt finds
that bookmakers may deliberately take outcome positions and exploit bettor
preferences instead of merely clearing the market.[^levitt] Franck et al.
describe book balancing as one end of a spectrum and note the difficulty and
risk of achieving it in practice.[^franck] Hegarty and Whelan show that using
overround as an expected-loss formula requires equal expected returns across
outcomes; favourite-longshot effects can violate that assumption.[^hegarty]

## References

[^wiki]: Wikipedia contributors, “Buchmacher,” *German Wikipedia*, revision of
    17 May 2026, <https://de.wikipedia.org/wiki/Buchmacher>. Accessed 4
    November 2026.

[^clarke]: Stephen Clarke, Stephanie Kovalchik, and Martin Ingram, “Adjusting
    Bookmaker's Odds to Allow for Overround,” *American Journal of Sports
    Science* 5(6), 2017, pp. 45–49.
    <https://doi.org/10.11648/j.ajss.20170506.12>.

[^hegarty]: Tadgh Hegarty and Karl Whelan, “Estimating Expected Loss Rates in
    Betting Markets: Theory and Evidence,” *Applied Economics* 58(28), 2026,
    pp. 5509–5523. <https://doi.org/10.1080/00036846.2025.2507979>.

[^levitt]: Steven D. Levitt, “Why Are Gambling Markets Organised So
    Differently from Financial Markets?,” *The Economic Journal* 114(495),
    2004, pp. 223–246.
    <https://doi.org/10.1111/j.1468-0297.2004.00207.x>.

[^franck]: Egon Franck, Erwin Verbeek, and Stephan Nüesch, “Prediction Accuracy
    of Different Market Structures—Bookmakers versus a Betting Exchange,”
    *International Journal of Forecasting* 26(3), 2010, pp. 448–459.
    <https://doi.org/10.1016/j.ijforecast.2010.01.004>.

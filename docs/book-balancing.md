# When can every outcome be profitable?

Yes: a bookmaker can have positive PnL no matter which outcome occurs when
the accepted stakes are sufficiently well balanced. The number of bets is not
the deciding factor. What matters is the total gross payout attached to each
outcome. This ideal is part of the introductory bookmaker account in the
German Wikipedia article [*Buchmacher*][wiki], but the exact conditions below
go beyond that overview.

## Source boundary

The baseline source explains fixed odds, locked accepted prices, reciprocal
odds, margin, and the idea of limiting risk by attracting stakes across all
outcomes.[^wiki] This page adds:

- an exact necessary-and-sufficient condition for all-positive scenario PnL;
- its expression in terms of stake shares and implied probabilities;
- a constructive equal-profit allocation for Bookie's proportional margin;
- the distinction between mathematical feasibility and observed bookmaker
  behaviour.

Those additions are explicit derivations from Bookie's accounting model.
Academic sources support the surrounding interpretation; the full mapping is
documented in [Sources, evidence, and scope](sources.md).

## The exact condition

Let:

- $S$ be the total of all accepted stakes;
- $G_i$ be the gross payout, including returned stakes, if outcome $i$ wins.

The bookmaker PnL in scenario $i$ is

$$
\operatorname{PnL}(i) = S-G_i.
$$

This is the same calculation as `RiskBook.worst_case_pnl()`: stakes on losing
outcomes minus the net liability on the winning outcome. Therefore the book
is profitable for **every** possible outcome exactly when

$$
G_i < S \quad\text{for every }i.
$$

When all bets on outcome $i$ have the same decimal odds $O_i$, let $S_i$ be
their combined stake and $w_i=S_i/S$ their share of the book. Then
$G_i=S_iO_i$, so the condition becomes

$$
w_i < \frac{1}{O_i} \quad\text{for every }i.
$$

In words: each outcome's share of accepted stakes must be smaller than its
probability implied by the offered odds. With bets accepted at different
locked odds, use the general gross-payout condition $G_i<S$ instead.

## Why overround makes this possible

The implied probabilities are $q_i=1/O_i$. They sum to more than one when
the odds contain an overround:

$$
\sum_i q_i=1+m>1.
$$

The sum of reciprocal decimal odds as the booksum, and its excess over one as
the overround, follows the standard definition used by Clarke, Kovalchik, and
Ingram.[^clarke]

Stake shares must sum to one, $\sum_i w_i=1$. The overround means the implied
probability limits have more than 100% of total capacity, so it is possible to
choose stake shares below every limit at once.

For the engine's proportional margin, $O_i=1/((1+m)p_i)$. If stakes arrive in
the fair-probability proportions $w_i=p_i$, every scenario has the same PnL:

$$
\operatorname{PnL}(i)
=S-S p_iO_i
=S\frac{m}{1+m}>0.
$$

For example, a total stake pool of 105 points with gross payouts of 100 points
for every outcome produces a guaranteed 5-point bookmaker profit. This is
often called a balanced book or a locked-in book.

## What is and is not guaranteed

- More bets can make balancing easier because stakes arrive in smaller pieces,
  but bet count alone guarantees nothing.
- A one-sided book can still lose in one scenario despite positive expected
  PnL.
- With zero overround, all scenarios can break even at best; they cannot all be
  strictly profitable. A positive overround creates the mathematical room for
  a strictly positive balanced result.
- The engine does not automatically rebalance or change prices from exposure.
  It reports scenario PnL and applies a configured risk floor to each proposed
  bet.
- Locked odds matter. Later price changes do not alter payouts on accepted
  bets.

So the observation is correct as a **possible state of a well-spread book**,
not as an automatic property of offering odds with a margin. Empirical work
also cautions against treating perfect balance as the universal real-world
business model: bookmakers may accept outcome exposure, price against bettor
preferences, or optimize expected profit rather than eliminate scenario
variance.[^levitt] [^franck] The conventional conversion from overround to
expected loss also relies on assumptions that can fail when margins differ by
outcome.[^hegarty]

[wiki]: https://de.wikipedia.org/wiki/Buchmacher

[^wiki]: Wikipedia contributors, “Buchmacher,” *German Wikipedia*, revision of
    17 May 2026, <https://de.wikipedia.org/wiki/Buchmacher>. Accessed 4
    November 2026. Used as introductory context; the page is itself flagged as
    lacking citations.

[^clarke]: Stephen Clarke, Stephanie Kovalchik, and Martin Ingram, “Adjusting
    Bookmaker's Odds to Allow for Overround,” *American Journal of Sports
    Science* 5(6), 2017, pp. 45–49,
    <https://doi.org/10.11648/j.ajss.20170506.12>.

[^levitt]: Steven D. Levitt, “Why Are Gambling Markets Organised So
    Differently from Financial Markets?,” *The Economic Journal* 114(495),
    2004, pp. 223–246,
    <https://doi.org/10.1111/j.1468-0297.2004.00207.x>.

[^franck]: Egon Franck, Erwin Verbeek, and Stephan Nüesch, “Prediction Accuracy
    of Different Market Structures—Bookmakers versus a Betting Exchange,”
    *International Journal of Forecasting* 26(3), 2010, pp. 448–459,
    <https://doi.org/10.1016/j.ijforecast.2010.01.004>.

[^hegarty]: Tadgh Hegarty and Karl Whelan, “Estimating Expected Loss Rates in
    Betting Markets: Theory and Evidence,” *Applied Economics* 58(28), 2026,
    pp. 5509–5523,
    <https://doi.org/10.1080/00036846.2025.2507979>.

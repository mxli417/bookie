"""
    Mini simulation of a random match with a bet market on each outcome. 
    Simulates a run with some gamblers on an arbitrary match and tests the
    functionality of the mini-bookie engine against that.
"""
import random
from bookie.engine.types import Market, Outcome, Bet
from bookie.engine.pricing import apply_margin, probs_to_odds
from bookie.engine.risk import RiskBook
from bookie.engine.accept import check_bet
from bookie.engine.settlement import settle

def sample_result(fair_probs):
    r = random.random()
    acc = 0.0
    for o, p in fair_probs.items():
        acc += p
        if r <= acc:
            return o
    return list(fair_probs.keys())[-1]

def simple_sim(random_seed: int = 1492, bookie_margin: float = 0.06, worst_case_pnl: float = -200.0):
    random.seed(random_seed)
    market = Market("M1", [Outcome.HOME, Outcome.DRAW, Outcome.AWAY])

    # set some "true" probabilities (unknown to bookmaker in real life)
    fair = {Outcome.HOME: 0.50, Outcome.DRAW: 0.25, Outcome.AWAY: 0.25}

    # set the bookie margin to 6 percent (or more) and see the adjusted quotes
    margin = bookie_margin
    implied = apply_margin(fair, margin)
    odds = probs_to_odds(implied)
    print("Odds:", odds, "Overround:", sum(1.0/o for o in odds.values()))

    book = RiskBook.empty(market.outcomes)
    bets = []

    # bettors: biased toward favorites (toy behavior)
    for i in range(80):
        if random.random() < 0.55:
            outcome = Outcome.HOME
        else:
            outcome = random.choice([Outcome.DRAW, Outcome.AWAY])

        # bettor stakes are fixed and arbitrary
        stake = random.choice([5, 10, 20])
        b = Bet(
            bet_id=f"B{i}", 
            market_id=market.market_id, 
            outcome=outcome, 
            stake=stake, 
            odds=odds[outcome]
        )

        # if engine accepts bet, add it to the book
        dec = check_bet(book, b, min_worst_case_pnl=worst_case_pnl)
        if dec.accepted:
            book.add_bet(b)
            bets.append(b)

    print("Worst-case PnL by outcome:", book.worst_case_pnl())
    result = sample_result(fair)
    total_pnl, _ = settle(bets, result)  # settle the book, i.e. pay or keep
    print("Match result:", result, "Bookmaker PnL:", round(total_pnl, 2))

# Quant Analysis Skill — Groww Bot Project

A skill for analyzing this project's trading data and results HONESTLY. Its
job is to keep every analysis consistent with the hard-won standards this
project has already paid for in bugs and retractions. Load this before doing
any data analysis, backtest interpretation, or strategy evaluation.

## The one rule that overrides everything

**Never manufacture or flatter a signal.** This project already caught one
fake profitable result (a stop-loss placed on the wrong side of entry created
a coin-flip that looked like +Rs17.76/trade edge; the bug fix flipped it to
-Rs16.08). The entire value of this system is that it tells the truth. An
analysis that produces a comforting but false result is worse than useless —
it's the thing that loses real money. When in doubt, report the less
exciting, more honest finding.

## What counts as "real edge" (the bar — do not lower it)

A (strategy, instrument) result is only real edge if ALL hold:
- **>= 30 trades** in the window (fewer = provisional, not a conclusion).
- **95% bootstrap confidence interval does not straddle zero.** A positive
  average with a CI of [-5, +20] is NOT edge — it's noise with an optimistic
  midpoint.
- **Net of realistic costs** — Indian fee schedule (brokerage, STT, exchange
  txn, SEBI fee, GST, stamp duty) AND slippage/spread. Gross P&L is never the
  answer.
- **Survives the multiple-comparisons check** (below).

State the numbers, the CI, and the trade count every single time. Never a bare
"it's profitable."

## The multiple-comparisons check (always apply when testing many things)

Testing N strategies/stocks/parameter-sets means ~5% of N will pass a 95% bar
by pure luck. Always report: "X passed; luck alone predicts ~0.05*N; therefore
[real signal / indistinguishable from noise / mixed]." If passes ≈ luck
baseline, the honest verdict is NOISE, not discovery. Getting ZERO passes
across a wide test is a clean, valuable negative — say so without hedging.

## Costs dominate at small size (correct the "it'll scale up" intuition)

Costs and bid-ask spread are a PERCENTAGE, so they hurt MORE at smaller
capital, not less. A strategy that "works" at Rs500 may be pure luck
overcoming a cost wall that vanishes at larger size; one that fails at Rs500
may work at Rs50,000. So: tiny/paper positions test the SYSTEM'S PLUMBING and
reaction time (does the order fire, does the stop attach on the right side,
does the dashboard update) — NOT the strategy's edge. Judge edge only from
replay backtests with modeled costs and thousands of trades. Never read the
P&L of a handful of tiny live trades as evidence about a strategy.

## Options-specific reasoning (the theta/vega trap)

An option's price = f(index move [delta], time decay [theta], IV change
[vega]). Indicators drawn on the OPTION's own price read direction through
theta+vega noise, so stop/support levels on the option chart are unreliable.
Correct pattern: signal on the INDEX (clean direction), size/stop/time-limit
on the OPTION PREMIUM (where the money is). Buyers fight theta — always use a
time-stop. When reporting option trade P&L, split it into direction vs
measured premium decay so the theta cost is visible. Lot size multiplies all
option P&L — and this project's lot-size history table is UNVERIFIED against
NSE circulars, so flag that caveat on any options result.

## Data integrity — assume nothing is clean

Before trusting any backtest, confirm: timestamps are IST and mark candle
OPEN (not close — a close-stamp shifts every signal one bar); options are
keyed by (underlying, expiry, strike, right), never a stitched continuous
series (rollovers create phantom jumps); gaps are marked NO-DATA, never
forward-filled into tradable bars (a scalper would "trade" prices that never
existed); equities are split/dividend adjusted (an unadjusted split looks like
a crash); the stock basket's survivorship bias is stated (today's constituents
inflate results). If any check fails, the result is untrustworthy — say so
before reporting numbers.

## Things that are BANNED

- Re-tuning a strategy that was tested and shown not to work, then re-testing
  on the same data until it passes. That's curve-fitting to noise and it
  manufactures a fake signal. Dead strategies stay dead; new ideas need a new
  hypothesis with a real reason to work.
- Putting an LLM or any slow/uncertain model in the trade-execution critical
  path. Signals can be advisory/slow-loop; execution is deterministic and
  fast. Risk envelope is immutable at runtime.
- Presenting synthetic (GBM) results as evidence of profitability. GBM is a
  random walk — every strategy's expected return there is zero minus costs;
  it tests PLUMBING, not EDGE. Label it as such.
- Any tiny local model (e.g. TRM) in the live signal path without first
  proving it in shadow against the full bar above. Verifiable-answer puzzle
  solvers do not inherit their edge on noisy, adversarial price data.

## Voice for analysis output

Plain, simple English a non-expert can follow. Full sentences. Explain what a
confidence interval means in words. Be decisive — commit to a verdict — but
always bind the verdict to the evidence, never to optimism. A clean negative
finding is a good outcome; report it plainly. Lead with the honest bottom line.
```

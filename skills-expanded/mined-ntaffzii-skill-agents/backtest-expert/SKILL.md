---
name: backtest-expert
description: Use this skill to simulate how a trading rule would have performed on historical price data — win rate, average return, max drawdown, profit factor — from a CSV or list of prices the user supplies, no market-data API required. Trigger on "backtest this strategy", "ทดสอบกลยุทธ์ย้อนหลัง", "how would this rule have performed historically", "moving average crossover backtest", "max drawdown of this strategy". If the user wants to size a position or apply a risk gate on a trade they're about to take, use position-sizer/drawdown-circuit-breaker instead — this skill evaluates a rule against the past, not a single upcoming trade.
---

# Backtest Expert

## Overview

[position-sizer](../position-sizer/SKILL.md) and [drawdown-circuit-breaker](../drawdown-circuit-breaker/SKILL.md) manage risk once you've already decided to trade a rule — neither tells you whether the rule itself actually works. This skill fills that gap: given historical price data and a set of buy/sell signals (either supplied directly or generated from a simple moving-average crossover), it simulates the trades a long-only, one-position-at-a-time strategy would have taken and reports the standard backtest metrics.

**Not financial advice.** A backtest describes how a rule performed on one specific historical sample. It does not predict future performance, and a rule tuned by trial-and-error against the same data it's being "backtested" on will look better than it is (overfitting/curve-fitting) — see Known limitations.

## When to use

- ทดสอบกฎเทรดกับข้อมูลราคาย้อนหลัง ก่อนใช้เงินจริง
- Evaluating a simple moving-average crossover (or any buy/sell signal series you already have) against historical prices
- Comparing win rate, average return, max drawdown, and profit factor across a few rule variants on the same data

## When NOT to use

- Sizing or risk-gating a specific upcoming trade — that's `position-sizer`/`drawdown-circuit-breaker`, not this skill
- The user wants live/real-time strategy execution — this is historical simulation only, it does not place or track live trades
- Short selling, multi-position, or portfolio-level backtesting — this engine is long-only and one-position-at-a-time; a strategy needing more than that needs a different tool

## Core knowledge

**Trade simulation**: long-only, one position at a time. Enters on a `"buy"` signal only while flat; exits on a `"sell"` signal only while in a position. A `"buy"` while already in a position, or a `"sell"` while flat, is a no-op — it does not pyramid into a second position or close a position that doesn't exist.

**Metrics reported**:

| Metric | Meaning |
|---|---|
| Win rate | % of completed trades with a positive return |
| Average return | Mean return % per completed trade |
| Total return | Compounded return across all trades, starting from a normalized equity of 1.0 |
| Max drawdown | Largest peak-to-trough decline in the equity curve across the whole run — same peak/current formula as [drawdown-circuit-breaker](../drawdown-circuit-breaker/SKILL.md) |
| Profit factor | Gross profit ÷ gross loss (sum of winning trades' returns over the absolute sum of losing trades' returns) — undefined (`None`) when there are no losing trades to divide by |

An open position at the end of the data (a `"buy"` with no later `"sell"`) is **not** counted as a completed trade and is flagged separately (`open_position_at_end`) — don't silently drop it from the report.

**Moving-average crossover signal generator**: a simple, common way to produce buy/sell signals mechanically instead of supplying them by hand. `fast_period`/`slow_period` are trailing-window sizes (in bars); a `"buy"` fires the first bar the fast MA moves above the slow MA, `"sell"` the first bar it moves below. No lookahead — each bar's MA only uses that bar and earlier ones. Bars without enough history for both MAs get `"hold"`.

## Common mistakes

1. Tuning the fast/slow period (or any rule parameter) by trying many values against the same historical sample and keeping whichever looks best — that's curve-fitting, not validation; the resulting metrics describe how well the rule was fit to this data, not how it will perform on new data.
2. Treating a high win rate as good on its own — a rule with a 70% win rate and rare large losses can still have a negative profit factor; report win rate, average return, and profit factor together, not in isolation.
3. Ignoring `open_position_at_end` — a trade still open when the data ends isn't a loss or a win, it's incomplete; don't fold it into win rate as either.
4. Applying this long-only, single-position engine to a strategy that actually shorts, pyramids, or holds multiple concurrent positions — the metrics would silently misrepresent a strategy this engine can't actually simulate.
5. Not accounting for what this backtest **excludes**: no commissions, slippage, taxes, or bid-ask spread by default — real returns will be lower than a raw backtest suggests, especially for a rule with many trades.

## Code

`backtest.py` — Decimal arithmetic, no dependencies:

- `run_backtest(bars)` → `BacktestResult(trades, total_trades, win_rate, avg_return_pct, total_return_pct, max_drawdown_pct, profit_factor, open_position_at_end)`, where `bars` is a chronological list of `{"date", "price", "signal"}`
- `generate_ma_crossover_signals(prices, fast_period, slow_period)` → the same list with a `"signal"` key added, ready to feed into `run_backtest`

Run `python3 backtest.py` for the self-test (includes a fully hand-verified trade sequence and a hand-verified MA-crossover signal sequence, not just round-trip assertions).

## Known limitations

- No commissions, slippage, spread, taxes, shorting, position sizing, or multi-position support — this is a minimal long-only single-position simulator, not a full trading-system backtester.
- Says nothing about statistical significance — a handful of trades on one historical window is a small sample; treat a backtest over a short period or few trades as weak evidence, not proof a rule works.
- Overfitting is a real, easy-to-fall-into trap: if the rule's parameters were chosen by testing many variants against this same data, the reported metrics are optimistic. A rule validated on data it was never tuned against (out-of-sample / walk-forward testing) is much stronger evidence — this skill does not enforce that discipline for you.
- Past performance shown by any backtest, however carefully done, does not guarantee future results.

---
name: trader-memory-core
description: Use this skill to log closed trades in a structured journal and compute win rate, average R-multiple, and expectancy from the trade history. Trigger on "trade journal", "log this trade", "win rate", "R-multiple", "expectancy", "trading stats". If the user just wants to record a trade with no analysis yet, this skill still applies — logging in the right schema now is what makes later stats possible.
---

# Trader Memory Core

## Overview

A trade without a record teaches nothing — the entire point of journaling is to make patterns visible across many trades (which setups actually work, whether stops get respected, whether sizing discipline holds) instead of relying on memory of a few vivid wins or losses. This skill defines a simple local journal schema and computes the standard trade-quality statistics from it: win rate, average R-multiple, and expectancy.

**Not financial advice.** This summarizes past results from data you supply; it does not predict future performance, and past win rate/expectancy are not guarantees.

## When to use

- บันทึกไม้เทรดที่ปิดแล้วลง journal
- คำนวณ win rate, R-multiple เฉลี่ย, expectancy จากประวัติการเทรด
- Reviewing whether stops/sizing were followed as planned across recent trades (pairs with a postmortem review of individual losing trades)

## When NOT to use

- The trade is still open — this skill's stats are for **closed** trades only; log the setup/plan when opening, but win/loss stats need an exit price
- The user wants a live P&L dashboard connected to a broker — this is a local structured-file journal, not a broker integration

## Core knowledge

**R-multiple**: the standard way to compare trades of different sizes on equal footing. `R = (exit_price - entry_price) / (entry_price - stop_price)` for a long trade — a +2R trade made twice its initial planned risk; a -1R trade lost exactly the planned risk (stop was hit cleanly); anything worse than -1R means the stop wasn't respected as planned or slippage occurred.

**Win rate**: fraction of trades with R > 0. On its own this is a weak metric — a strategy can have a low win rate and still be strongly profitable if average wins are large relative to average losses (or vice versa), which is why **expectancy** matters more than win rate alone.

**Expectancy** (in R-multiples): `win_rate × avg_win_R + loss_rate × avg_loss_R` (avg_loss_R is negative, so this naturally nets losses against wins). A positive expectancy means the strategy makes money on average per trade, over this sample — it is a backward-looking summary of the logged trades, not a forward guarantee.

**Journal schema** (`journal-schema.yaml`): one entry per closed trade — ticker, direction, setup tag, entry/stop/exit, R-multiple, and free-text notes/mistake tags. Recording the **original** stop (not a trailed one) is what makes the R-multiple meaningful as "did this trade perform relative to its initial plan."

## Common mistakes

1. Computing R-multiple against a trailed/moved stop instead of the original planned stop — this hides whether the original risk plan was actually respected.
2. Reporting win rate alone as "how good the strategy is" without expectancy — a 70% win rate with tiny wins and rare huge losses can still have negative expectancy.
3. Only journaling losing trades (to "figure out what went wrong") — winning trades need review too, especially to check whether wins were the result of the plan working or of luck/oversized risk that happened to pay off.
4. Treating past expectancy (computed from a small sample) as a guarantee of future results.
5. Logging trades sporadically rather than consistently — stats computed from a partial/biased sample of trades (e.g. only remembering to log the dramatic ones) will misrepresent the actual track record.

## Code

`journal_stats.py` — pure Decimal arithmetic, no dependencies:

- `compute_r_multiple(entry, stop, exit_price)` → Decimal R-multiple for one trade
- `compute_trade_stats(trades)` → `TradeStats(total_trades, wins, losses, breakeven, win_rate, avg_r_multiple, avg_win_r, avg_loss_r, expectancy_r)`

`journal-schema.yaml` — the per-trade record schema with a synthetic example entry.

Run `python3 journal_stats.py` for the self-test.

## Known limitations

- This skill computes statistics from a journal the user maintains; it does not connect to a broker or verify entries against real fills.
- Small sample sizes produce statistically unreliable win-rate/expectancy figures — flag this when a user has only a handful of logged trades, rather than presenting the number as settled.
- Does not itself store data persistently across sessions — the user (or the surrounding tool/workflow) owns the actual journal file.

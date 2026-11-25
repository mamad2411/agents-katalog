---
name: earnings
description: Prepares for a scheduled earnings release by measuring the move the options market implies from the at the money straddle and comparing it with the stock's realized moves on past release days. Use when asked what move is priced in for earnings, what the implied or expected move is, how a stock usually moves on earnings, or how the options market compares with history.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Earnings preparation

Answers one question: what is expected from this earnings release? Every number comes from the scripts.

## Inputs

- Spot price of the stock, taken at the same time as the option quotes.
- Either the at the money call and put prices (mids) for the first expiry after the release, or an option chain CSV with columns `expiry, strike, type, bid, ask`.
- The reaction date: the first session that trades on the release. For a release before the open it is the release date; after the close it is the next session.
- For history: `prices.csv` (date column, then daily closing prices) and `events.csv` with columns `date, timing`, where timing is `bmo` (before the open) or `amc` (after the close).

Never estimate option prices or past release dates from memory. Ask for them.

## Procedure

1. Confirm the release date, its timing, and the reaction date.
2. Measure the implied move:
   ```bash
   python scripts/implied_move.py --spot 182.40 --chain chain.csv --reaction-date 2025-07-31
   ```
   or with two prices: `--spot 182.40 --call 6.10 --put 5.85 --strike 182.5`.
3. Measure past reactions and compare:
   ```bash
   python scripts/historical_moves.py --prices prices.csv --asset XYZ --events events.csv --implied 0.0655
   ```
   Pass the `implied_move_pct` from step 2 as `--implied`.
4. Report the implied move, the historical moves, and their ratio. After the release, hand the event to the events skill to measure the reaction.

## Checks

- Quotes are valid (bid not above ask), the strike is within 2.5% of spot, and the expiry falls within a week of the reaction date.
- At least four past releases were measured, and every listed release was found in the price data.

## Output

`implied_move.py`: `results.implied_move` (in price), `results.implied_move_pct`, the straddle breakevens, and the quotes used. `historical_moves.py`: each past move with its dates, `mean_abs_move`, `median_abs_move`, `max_abs_move`, `share_up`, and with `--implied` the ratio of implied to mean move and the share of past moves that exceeded it.

## Explaining the result

- Lead with the implied move in percent and in price, then the historical mean and median.
- A ratio above one means the options price a larger move than the stock has typically made; below one, a smaller move.
- The straddle prices the expected absolute move, not the direction. Report the share of past moves that were up only as history.
- The straddle also holds the time value of days that are not the release. Expiries close to the release keep that small; the check flags distant ones.

For the approximation and timing rules, see [references/methodology.md](references/methodology.md).

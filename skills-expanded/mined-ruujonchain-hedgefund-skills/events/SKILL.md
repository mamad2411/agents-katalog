---
name: events
description: Measures how the market priced a dated event such as earnings, guidance, or a rating change. Use when asked how a stock reacted to news, whether a move after an announcement was abnormal or significant, or for an event study, abnormal return, CAR, or post announcement reaction.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Event study

Answers one question: how did the market price this news? Uses the market model event study (MacKinlay, 1997). Every number comes from the scripts.

## Inputs

- `prices.csv`: a date column, then total return price levels (dividends reinvested) for the security and for a market index. Daily, complete, no gaps.
- The security column, the market column, and the event date.
- Day 0 is the first trading session on or after the event date. If the news came after the close, use the next session's date as the event date and say so.
- At least 270 trading days of prices before the event.

If the user names a stock and date but provides no prices, ask for them. Never fill gaps or invent prices.

## Procedure

1. Resolve the security, the market index, and the event date (adjust for releases after the close).
2. Fit the market model on 250 days ending 20 days before the event:
   ```bash
   python scripts/fit_market_model.py --prices prices.csv --asset XYZ --market INDEX \
     --event-date 2025-05-01 --out fit.json
   ```
3. Compute AR, CAR and t over the event window (default days -1 to +1):
   ```bash
   python scripts/car.py --fit fit.json --window -1 1
   ```
   Use `--window 0 0` for the announcement day alone, or a longer window such as `0 5` to study drift.
4. Report CAR, t, the windows used, and the check results.

## Checks

- The estimation window is complete and ends before the event window begins (windows never overlap).
- Prices are positive, complete total return levels.
- The event window lies inside the data, and day 0 matches the fit.

If any check fails, report it and stop.

## Output

`car.py` returns `results.car`, `results.t_stat`, `results.p_value_normal`, the daily abnormal returns, and the fitted alpha, beta and residual volatility, plus `checks` and `passed`.

## Explaining the result

- State the CAR as a percentage, the window, and the t statistic. Values of t beyond about 2 in absolute size are unusual under normal day to day noise.
- Separate the abnormal move from the market move: the market model removes what the index explains.
- One event is a single observation. Confounding news in the same window (another announcement, an index change) can drive the result; mention it when known.

For the mathematics and design choices, see [references/methodology.md](references/methodology.md).

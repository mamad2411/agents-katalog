---
name: sizing
description: Turns an expected return and a risk estimate into a position size using fractional Kelly, a volatility target, and a maximum weight. Use when asked how large a position should be, how to size or scale a strategy, what the Kelly fraction is, or how to bring a position to a target volatility.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Position sizing

Answers one question: how large should this position be? Combines the Kelly criterion (Kelly, 1956) with volatility targeting. Every number comes from `scripts/size.py`.

## Inputs

- `mu`: annual expected return in excess of cash, as a decimal. This is the user's own estimate. Never supply one yourself; if it is missing, ask.
- Risk, one of:
  - `sigma`: annual volatility as a decimal, or
  - a returns file (date column, then simple returns) plus the column to use. Daily data is assumed; set `--periods-per-year` otherwise.
- Optional: Kelly fraction (default 0.5), target volatility for the position, maximum absolute weight (default 1.0).

## Procedure

1. Confirm mu, its horizon (annual), and that it is in excess of cash.
2. Run the sizing:
   ```bash
   python scripts/size.py --mu 0.06 --sigma 0.25 --kelly-fraction 0.5 --target-vol 0.10
   ```
   or estimate sigma from history:
   ```bash
   python scripts/size.py --mu 0.06 --returns returns.csv --column XYZ --halflife 63 --target-vol 0.10
   ```
3. Read the JSON. If `passed` is false, report the failed check and stop.
4. Report the weight, which constraint set it, and the inputs behind it.

## Checks

- The full Kelly fraction satisfies its closed form, mu = f* sigma squared.
- The weight respects the maximum weight.
- Position volatility does not exceed the target, when one is given.

## Output

`results.weight` (signed fraction of capital), `results.binding_constraint` (`kelly`, `target_vol`, or `max_weight`), `full_kelly`, `fractional_kelly`, `vol_target_weight`, `position_volatility`, `expected_growth`, and `share_of_max_growth`, plus `checks` and `passed`.

## Explaining the result

- Lead with the weight and the constraint that set it. Kelly sizes the conviction; the volatility target and maximum weight cap the risk.
- Half Kelly earns three quarters of the maximum growth rate with half the volatility of full Kelly, which is why fractional Kelly is the default when mu is uncertain.
- The result is only as good as mu. Show how the weight changes if mu is half as large; rerun the script for that case rather than estimating it.
- This sizes one position in isolation. For a portfolio, use the risk skill to see how the position changes total risk.

For the mathematics, see [references/methodology.md](references/methodology.md).

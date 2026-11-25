---
name: validation
description: Tests whether a backtest result reflects skill or the luck of trying many variations, using the probabilistic Sharpe ratio and the deflated Sharpe ratio, which adjust for track length, skewness, fat tails, and the number of trials. Use when asked whether a backtest or Sharpe ratio is real, significant, overfit, or worth trusting, or how long a track record needs to be.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Strategy validation

Answers one question: is this backtest result real? Uses the probabilistic Sharpe ratio (Bailey and López de Prado, 2012) and the deflated Sharpe ratio (Bailey and López de Prado, 2014). Every number comes from `scripts/psr_dsr.py`.

## Inputs

- `returns.csv`: a date column, then periodic returns of the selected strategy (net of costs, excess of cash if available). Complete, no gaps.
- The number of trials: every variation tested on the way to this result, including parameter sets, universes, and rules that were discarded. This input is required. If the user does not know it, ask for their best honest count and state it in the answer.
- The dispersion of results across trials, one of:
  - the returns of all trials (`--trial-returns`), or
  - their per period Sharpe ratios (`--trial-sharpes`), or
  - the variance of per period Sharpe ratios (`--sr-variance`) together with `--trials`.

## Procedure

1. Confirm the selected strategy, the return frequency, and the number of trials.
2. Run the validation:
   ```bash
   python scripts/psr_dsr.py --returns returns.csv --column STRAT \
     --trial-returns all_trials.csv --periods-per-year 252
   ```
   or, without trial returns:
   ```bash
   python scripts/psr_dsr.py --returns returns.csv --column STRAT --trials 40 --sr-variance 0.0004
   ```
3. Read the JSON. If `passed` is false, report the failed check and stop.
4. Report the Sharpe ratio, PSR, the threshold SR0, DSR, and whether DSR clears the confidence level.

## Checks

- At least 60 observations.
- The trial count is at least the number of trials supplied.
- The variance term in the PSR formula is positive.

## Output

`results.sharpe_per_period`, `results.sharpe_annualized`, `skewness`, `kurtosis` (3 for normal returns), `psr` against the benchmark, `sr0_per_period` and `sr0_annualized` (the Sharpe ratio the best of N trials would reach by chance), `dsr`, `passes`, and `min_track_record_length` in periods, plus `checks` and `passed`.

## Explaining the result

- Lead with DSR: the probability that the true Sharpe ratio exceeds what the best of N luckless trials would show. A DSR of 0.95 or more clears the default bar.
- Compare the annualized Sharpe with the annualized SR0, so the reader sees how high the bar was raised by the search.
- Negative skew and fat tails lower PSR and DSR for the same Sharpe ratio. Say so when they matter.
- Minimum track record length is the number of periods needed for DSR to reach the confidence level at the current Sharpe ratio.
- A failing DSR does not prove the idea is wrong. It shows the evidence is not yet strong enough given the search behind it.

For formulas and conventions, see [references/methodology.md](references/methodology.md).

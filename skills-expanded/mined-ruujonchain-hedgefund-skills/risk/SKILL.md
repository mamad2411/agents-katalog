---
name: risk
description: Decomposes the volatility of a portfolio into the contribution of each position and, with a factor model, of each factor and of specific risk. Use when asked where the risk in a portfolio comes from, which positions or factors drive volatility, what the portfolio's factor exposures are, or which trades would reduce risk most efficiently.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Factor risk decomposition

Answers one question: where does the risk in this portfolio come from? Every number comes from `scripts/decompose.py`. Never compute volatility or contributions yourself.

## Inputs

- `weights.csv` with columns `asset, weight`. Weights are fractions of capital; shorts are negative.
- One source of risk, in this order of preference:
  1. Factor model: `exposures.csv` (asset rows, factor columns), `factor_cov.csv` (factor by factor), `specific_var.csv` (columns `asset, specific_var`).
  2. Full covariance: `cov.csv` (asset by asset).
  3. Historical returns: `returns.csv` (date column, then one column of simple returns per asset). Use only when no model is available, and say so in the answer.
- Every input must be known as of the analysis date. Do not mix a covariance estimated today with weights from another day without saying so.
- State the units. Covariances are annual unless `--periods-per-year` says otherwise. Returns mode assumes daily data (252).

If the user has not provided weights or a risk source, ask for them. Never invent covariances or exposures.

## Procedure

1. Confirm the analysis date, the weights file, and which risk source is available.
2. Run the decomposition:
   ```bash
   python scripts/decompose.py --weights weights.csv \
     --exposures exposures.csv --factor-cov factor_cov.csv --specific-var specific_var.csv
   ```
   Alternatives: `--cov cov.csv`, or `--returns returns.csv` (add `--periods-per-year 52` for weekly data).
3. Read the JSON. If `passed` is false, report which check failed and stop.
4. Report the total volatility, the largest position contributions, and, in factor mode, the factor and specific split.

## Checks

The script verifies, and the agent reports when any fails:
- The covariance is positive semidefinite.
- Position contributions sum exactly to total volatility.
- In factor mode, factor plus specific contributions sum exactly to total volatility.

## Output

JSON with `results.total_volatility`, `results.positions` (weight, marginal risk, contribution, share), and in factor mode `results.factors`, `results.factor_total`, `results.specific_total`, plus `checks` and `passed`. Shares sum to one; a negative share means the position hedges the rest of the book.

## Explaining the result

- Lead with total volatility and the share explained by the top three positions.
- Contribution equals weight times marginal risk. A position with high marginal risk is where a small trade changes total risk most; a negative marginal risk means adding to that position lowers total risk.
- In factor mode, say how much risk is systematic versus specific, and name the factor with the largest share.
- Volatility is a forecast from the supplied model, not an observed outcome. Name the model or estimation window used.

For the mathematics and conventions, see [references/methodology.md](references/methodology.md).

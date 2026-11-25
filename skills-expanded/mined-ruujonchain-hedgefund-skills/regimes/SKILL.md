---
name: regimes
description: Estimates which market regime is in force, as a probability for each regime, from relative features such as the ratio of short to long volatility, trend strength, drawdown, and cross asset correlation, using only data available at each date. Use when asked what kind of market we are in, whether volatility or stress is rising, for regime probabilities, or for exposure that adapts to the regime.
license: MIT
compatibility: Requires Python 3.9 or later with numpy and pandas.
metadata:
  owner: research
  version: "1.0"
---

# Regime detection

Answers one question: what kind of market are we in? Fits a Gaussian hidden Markov model (Hamilton, 1989) to relative features and reports filtered probabilities. Every number comes from `scripts/regimes.py`.

## Inputs

- `prices.csv`: a date column, then daily price levels. One column is the series whose regime is measured (for example an equity index). Extra columns, such as bonds, credit, or currencies, feed the average correlation feature.
- At least three years of daily history: one year to warm up the features and enough to train and then report.
- A training end date. The model is fitted only on data up to that date; report dates after it are out of sample. If the user gives none, the script uses the midpoint of the history and flags it.
- Optional: a target exposure for each regime, ordered from lowest to highest volatility. These are the user's own policy. Never propose them yourself.

## Procedure

1. Confirm the series, the correlation series, the number of regimes (2 or 3), and the training end date.
2. Run the model:
   ```bash
   python scripts/regimes.py --prices prices.csv --asset INDEX --states 3 \
     --train-end 2019-12-31 --exposures 1.0,0.6,0.2 --history regimes_history.csv
   ```
3. Read the JSON. If `passed` is false, report the failed check and stop.
4. Report the probability of each regime, the most likely regime, the feature values behind it, and the blended exposure when targets were given.

## Checks

- Probabilities sum to one on every date.
- No future data: probabilities recomputed from prices cut at a check date match the full run exactly.
- The EM fit converged.
- The report date lies after the training period.

## Output

`results.probabilities` (one per regime: `low_vol`, `normal`, `high_vol`, or two of them), `results.most_likely`, `results.features`, `results.regime_means`, `results.transition_matrix`, `results.expected_duration_days`, and with targets `results.blended_exposure`. `--history` writes the daily probabilities to a CSV.

## Explaining the result

- Lead with the probabilities, not only the most likely label; a 55 to 45 split is a different message from 95 to 5.
- Tie the answer to the features: for example, short term volatility running above its one year level with a falling trend and rising correlation.
- Regimes are labeled by their average volatility ratio. Describe them with the `regime_means`, which show what each regime looked like in training.
- Expected duration comes from the transition matrix and describes typical persistence in the training period.
- The blended exposure moves smoothly as probabilities change, which avoids abrupt switches on noisy signals.

For features, the model, and the filter, see [references/methodology.md](references/methodology.md).

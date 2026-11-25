---
name: arima-fraud-detection-eval
description: Evaluates unsupervised anomaly detection models on credit card transaction time series to identify fraudulent spending deviations. It probes the ability of models to balance precision and recall in highly imbalanced, real-world financial data without relying on labeled fraud examples. Use when the user wants to benchmark on Credit card transaction time series, or asks about evaluating this task. Reports F-Measure.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2009.07578
  bibtex_key: moschini2020anomaly
  confidence: high
---

# arima-fraud-detection-eval

> Anomaly and Fraud Detection in Credit Card Transactions Using the ARIMA Model — Moschini et al. (2020) (arXiv:2009.07578, 2020)

## What this evaluates

Evaluates unsupervised anomaly detection models on credit card transaction time series to identify fraudulent spending deviations. It probes the ability of models to balance precision and recall in highly imbalanced, real-world financial data without relying on labeled fraud examples.

## Datasets

- **Credit card transaction time series** — total ?; splits: test (-1)

## Metrics

- `Precision` — range: percent
  - True Positive / (True Positive + False Positive). Measures the proportion of predicted frauds that are actually frauds.
- `Recall` — range: percent
  - True Positive / (True Positive + False Negative). Measures the proportion of actual frauds correctly identified by the model.
- `F-Measure` **(primary)** — range: percent
  - 2 * (Precision * Recall) / (Precision + Recall). Harmonic mean of Precision and Recall used as the headline performance metric.

## Input / output format

**Input**: Daily transaction count time series per customer, analyzed using rolling windows to model normal spending behavior.

**Output**: Binary classification per time point indicating predicted anomaly/fraud.

## Scoring recipe

```python
tp = sum(pred == 1 and gold == 1)
fp = sum(pred == 1 and gold == 0)
fn = sum(pred == 0 and gold == 1)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
# Average across all time series
avg_precision = mean(precision_list)
avg_recall = mean(recall_list)
avg_f1 = mean(f1_list)
```

## Common pitfalls

- Only 9 out of 24 time series contained real frauds in the original test set, requiring synthetic fraud injection for the remainder.
- Performance heavily depends on the number of injected fraudulent counts (1-8) and the specific day chosen, necessitating 100 random repetitions per series to compute averages.
- LOF underperforms significantly because it was designed for multidimensional datasets, not univariate daily transaction counts.

## Evidence (verbatim from paper)

> The results are presented based on three metrics: Precision, Recall and F-Measure. Precision refers to the ability of the model to be trustworthy as regards its classified positive points; that is, Precision tells us how many of the predicted frauds are actually frauds. A high Precision means that when the model classifies a point as positive it is highly likely that it is a correct classification. ... These metrics are calculated for each of the 9 time series analysed and used to obtain the average as described in the previous section.

## Citation

```bibtex
@misc{moschini2020anomaly,
  title={Anomaly and Fraud Detection in Credit Card Transactions Using the ARIMA Model},
  author={Moschini et al. (2020)},
  year={2020},
  note={arXiv:2009.07578}
}
```

- arXiv: 2009.07578

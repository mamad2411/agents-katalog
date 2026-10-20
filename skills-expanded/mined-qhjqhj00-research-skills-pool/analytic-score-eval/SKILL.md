---
name: analytic-score-eval
description: Evaluates the scoring accuracy of interpretable automated scoring frameworks on educational assessment items across three domains. It measures how well LLM-extracted features and ordinal logistic regression align with human raters while adhering to strict interpretability constraints. Use when the user wants to benchmark on Educational Assessment Items (Science, Reading Informational Text, Reading Literature), or asks about evaluating this task. Reports QWK.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.17069
  bibtex_key: kim2025principled
  confidence: high
---

# analytic-score-eval

> Principled Design of Interpretable Automated Scoring for Large-Scale Educational Assessments — Kim et al. (2025) (arXiv:2511.17069, 2025)

## What this evaluates

Evaluates the scoring accuracy of interpretable automated scoring frameworks on educational assessment items across three domains. It measures how well LLM-extracted features and ordinal logistic regression align with human raters while adhering to strict interpretability constraints.

## Datasets

- **Educational Assessment Items (Science, Reading Informational Text, Reading Literature)** — total ?; splits: test (-1)

## Metrics

- `QWK` **(primary)** — range: [0, 1]
  - Quadratic Weighted Kappa measures agreement between predicted and human scores, penalizing disagreements quadratically based on the distance between score categories. It is the headline metric for scoring accuracy.
- `Label-wise F1` — range: [0, 1]
  - F1 score computed independently for each discrete score label (0, 1, 2) to evaluate per-class prediction performance.

## Input / output format

**Input**: Raw student response text for an assessment item, categorized by domain (Science, Reading Informational Text, or Reading Literature).

**Output**: A discrete ordinal score (0, 1, or 2) indicating response quality, derived from LLM-extracted featurized values passed through an ordinal logistic regression model.

## Scoring recipe

```python
def compute_qwk(preds, gold):
    # Quadratic Weighted Kappa: penalizes errors quadratically based on distance between predicted and true scores
    # preds, gold: lists/arrays of integers 0, 1, 2
    return quadratic_weighted_kappa(gold, preds)

def compute_f1(preds, gold):
    # Label-wise F1: computes F1 score for each score category (0, 1, 2)
    f1_scores = {}
    for label in [0, 1, 2]:
        y_true = [1 if g == label else 0 for g in gold]
        y_pred = [1 if p == label else 0 for p in preds]
        f1_scores[label] = f1_score(y_true, y_pred, zero_division=0)
    return f1_scores
```

## Common pitfalls

- QWK is heavily influenced by severe class imbalance (label 0 dominates), so high QWK can mask poor performance on higher-score categories.
- Label-wise F1 for label 1 is consistently low due to category ambiguity and rarity, which should not be interpreted as model failure but as a task design limitation.
- Reported QWK and F1 values include 95% bootstrap confidence intervals; comparing point estimates without considering interval overlap can lead to false significance claims.

## Evidence (verbatim from paper)

> Across items and within each assessment area, AnalyticScore outperforms several automated scoring baselines on average and, given its interpretability, achieves reasonable performance compared to state-of-the-art black-box models. Compared to the best-performing models in each assessment area, AnalyticScore is, on average, within 0.06 QWK for all items, 0.04 QWK for Science, 0.08 QWK for Reading (Informational Text), and 0.09 QWK for Reading (Literature) items.

## Citation

```bibtex
@misc{kim2025principled,
  title={Principled Design of Interpretable Automated Scoring for Large-Scale Educational Assessments},
  author={Kim et al. (2025)},
  year={2025},
  note={arXiv:2511.17069}
}
```

- arXiv: 2511.17069

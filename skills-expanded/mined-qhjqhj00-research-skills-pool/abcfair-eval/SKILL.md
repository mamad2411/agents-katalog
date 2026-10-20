---
name: abcfair-eval
description: Evaluates the trade-off between predictive performance and fairness across diverse real-world settings. It probes how different intervention stages, sensitive feature compositions, fairness notions, and output distributions impact a model's ability to satisfy fairness constraints while maintaining accuracy. Use when the user wants to benchmark on SchoolPerformance, ACSPublicCoverage, or asks about evaluating this task. Reports AUROC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.16965
  bibtex_key: defrance2024abcfair
  confidence: high
---

# abcfair-eval

> ABCFair: an Adaptable Benchmark approach for Comparing Fairness Methods — Defrance et al. (2024) (arXiv:2409.16965, 2024)

## What this evaluates

Evaluates the trade-off between predictive performance and fairness across diverse real-world settings. It probes how different intervention stages, sensitive feature compositions, fairness notions, and output distributions impact a model's ability to satisfy fairness constraints while maintaining accuracy.

## Datasets

- **SchoolPerformance** — total ?; splits: train (-1), test (-1)
- **ACSPublicCoverage** — total ?; splits: train (-1), test (-1)

## Metrics

- `Accuracy` — range: [0, 1]
  - Proportion of correctly classified instances on the test set.
- `AUROC` **(primary)** — range: [0, 1]
  - Area under the Receiver Operating Characteristic curve, measuring ranking quality for soft predictions.
- `Demographic Parity Violation` — range: [0, 1]
  - Maximum difference in positive prediction rates across sensitive groups (soft or hard).
- `Equal Opportunity Violation` — range: [0, 1]
  - Maximum difference in true positive rates across sensitive groups.

## Input / output format

**Input**: Tabular features and labels (biased and/or unbiased) from SchoolPerformance or ACSPublicCoverage, along with sensitive attribute values.

**Output**: Model predictions (hard binary labels or soft probability scores) and computed fairness violation metrics.

## Scoring recipe

```python
def compute_metrics(preds, labels, sensitive, k, notion='demographic_parity'):
    # Performance metric
    acc = np.mean(preds == labels) if preds.ndim == 1 else roc_auc_score(labels, preds)
    
    # Fairness violation
    groups = np.unique(sensitive)
    rates = [np.mean(preds[sensitive == g]) for g in groups]
    violation = max(rates) - min(rates)
    
    # Constraint check
    if violation <= k:
        return acc, violation
    return None, violation
```

## Common pitfalls

- Evaluating accuracy on biased labels instead of the dual unbiased labels obscures the true accuracy-fairness synergy.
- Directly comparing methods that output hard binary predictions against those outputting soft scores without accounting for output distribution differences.
- Ignoring the specific fairness notion and sensitive feature composition (binary vs. intersectional) when reporting violation bounds.

## Evidence (verbatim from paper)

> Table 4: The maximal AUROC and standard error in %, for the fairness strength where the (soft) demographic parity violation is smaller than k. A naive model achieves AUROC=81.2% and fairness violation of Binary=0.046, Intersectional=0.48 and Parallel=0.17.

## Citation

```bibtex
@misc{defrance2024abcfair,
  title={ABCFair: an Adaptable Benchmark approach for Comparing Fairness Methods},
  author={Defrance et al. (2024)},
  year={2024},
  note={arXiv:2409.16965}
}
```

- arXiv: 2409.16965

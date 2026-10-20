---
name: arabic-claim-verification-eval
description: This benchmark evaluates a model's ability to classify the veracity of Arabic social media claims as true or false. It probes factual consistency and reasoning against reliable sources in a binary classification setting. Use when the user wants to benchmark on Arabic Claim Verification Dataset, or asks about evaluating this task. Reports Macro-F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.07997
  bibtex_key: barroncedeno2020checkthat
  confidence: high
---

# arabic-claim-verification-eval

> Overview of CheckThat! 2020: Automatic Identification and Verification of Claims in Social Media — Barrón-Cedeno et al. (2020) (arXiv:2007.07997, 2020)

## What this evaluates

This benchmark evaluates a model's ability to classify the veracity of Arabic social media claims as true or false. It probes factual consistency and reasoning against reliable sources in a binary classification setting.

## Datasets

- **Arabic Claim Verification Dataset** — total 165; splits: test (165)

## Metrics

- `Macro-F1` **(primary)** — range: [0, 1]
  - Macro-averaged F1 score, computed as the unweighted mean of the F1 scores for the 'true' and 'false' classes.

## Input / output format

**Input**: Arabic claim text.

**Output**: Binary label: 'true' or 'false'.

## Scoring recipe

```python
def score(predictions, gold):
    tp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 1)
    fp = sum(1 for p, g in zip(predictions, gold) if p == 1 and g == 0)
    fn = sum(1 for p, g in zip(predictions, gold) if p == 0 and g == 1)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    return f1
```

## Common pitfalls

- The dataset is highly imbalanced (only 6 false claims out of 165), so accuracy is misleading; macro-F1 is required.
- Only definite true/false labels were used; partially-true claims were excluded.

## Evidence (verbatim from paper)

> We treated the task as a classification problem and we used typical evaluation measures for such tasks in the case of class imbalance: Precision, Recall, and F1 score. The latter was the official evaluation measure.

## Citation

```bibtex
@misc{barroncedeno2020checkthat,
  title={Overview of CheckThat! 2020: Automatic Identification and Verification of Claims in Social Media},
  author={Barrón-Cedeno et al. (2020)},
  year={2020},
  note={arXiv:2007.07997}
}
```

- arXiv: 2007.07997

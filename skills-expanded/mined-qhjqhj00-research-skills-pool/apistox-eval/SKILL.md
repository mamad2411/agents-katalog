---
name: apistox-eval
description: Evaluates the ability of molecular graph machine learning models and fingerprint-based methods to predict binary pesticide toxicity to honey bees. It specifically probes domain generalization by testing performance on structurally novel compounds and temporally separated data rather than random splits. Use when the user wants to benchmark on ApisTox, or asks about evaluating this task. Reports MCC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.18703
  bibtex_key: adamczyk2025apistox
  confidence: high
---

# apistox-eval

> Towards Rational Pesticide Design with Graph Machine Learning Models for Ecotoxicology — Adamczyk et al. (2025) (arXiv:2509.18703, 2025)

## What this evaluates

Evaluates the ability of molecular graph machine learning models and fingerprint-based methods to predict binary pesticide toxicity to honey bees. It specifically probes domain generalization by testing performance on structurally novel compounds and temporally separated data rather than random splits.

## Datasets

- **ApisTox** — total 1035; splits: MaxMin split (-1), Time split (-1)

## Metrics

- `MCC` **(primary)** — range: [-1, 1]
  - Matthews correlation coefficient for binary classification. It measures the correlation between observed and predicted binary classifications, accounting for true/false positives and negatives. It is robust to class imbalance.

## Input / output format

**Input**: Molecular structures provided as SMILES strings.

**Output**: Binary classification label: toxic or non-toxic.

## Scoring recipe

```python
def compute_mcc(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    numerator = tp * tn - fp * fn
    denominator = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return numerator / denominator if denominator != 0 else 0.0
```

## Common pitfalls

- The dataset is moderately imbalanced (29% positive cases), so accuracy is misleading; MCC is explicitly chosen to handle this.
- Splits are domain-specific: 'MaxMin split' tests generalization to novel chemical scaffolds, and 'Time split' tests generalization to future compounds, making direct comparison with random-split benchmarks invalid.

## Evidence (verbatim from paper)

> It consists of 1035 pesticide molecules in SMILES format with binary toxic/non-toxic labels, following US EPA guidelines. It is moderately imbalanced, with 29% positive cases. Compared to previous datasets (e.g., CropCSM, BeeTox), it is the largest and the only one free of invalid entries or structural duplicates. The initial classification results are presented in Table [1], with more details in the preprint (Adamczyk et al., [2025b]). Five top-performing molecular fingerprints were selected for brevity. Matthews correlation coefficient (MCC) was used as an evaluation metric, as it works well for imbalanced classification.

## Citation

```bibtex
@misc{adamczyk2025apistox,
  title={Towards Rational Pesticide Design with Graph Machine Learning Models for Ecotoxicology},
  author={Adamczyk et al. (2025)},
  year={2025},
  note={arXiv:2509.18703}
}
```

- arXiv: 2509.18703

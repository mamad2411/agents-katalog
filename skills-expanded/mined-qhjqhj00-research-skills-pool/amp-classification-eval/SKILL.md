---
name: amp-classification-eval
description: Evaluates the ability of reprogrammed language models to classify antimicrobial peptide (AMP) sequences into binary categories (toxic vs. non-toxic, or AMP vs. non-AMP) using limited labeled data. Use when the user wants to benchmark on AMP Dataset, or asks about evaluating this task. Reports Test Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2012.03460
  bibtex_key: vinod2020reprogramming
  confidence: high
---

# amp-classification-eval

> Reprogramming Language Models for Molecular Representation Learning — Vinod et al. (2020) (arXiv:2012.03460, 2020)

## What this evaluates

Evaluates the ability of reprogrammed language models to classify antimicrobial peptide (AMP) sequences into binary categories (toxic vs. non-toxic, or AMP vs. non-AMP) using limited labeled data.

## Datasets

- **AMP Dataset** — total 10192; splits: train (8153), valid (1019), test (1020)

## Metrics

- `Test Accuracy` **(primary)** — range: percent
  - Percentage of correctly classified instances in the test set. Calculated as (number of correct predictions) / (total number of test instances) * 100.

## Input / output format

**Input**: Character-level tokenized AMP sequences (7 distinct tokens) fed into a reprogrammed language model (e.g., BERT).

**Output**: Binary classification label: 'Toxic' or 'Non-Toxic' for toxicity prediction; 'AMP' or 'Non-AMP' for AMP prediction.

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Evaluating on fewer than 5000 training samples yields statistically insignificant accuracy (~random chance) for both R2DL and baselines.
- Increasing k-SVD iterations beyond 100 does not improve test accuracy but significantly increases computational cost.
- The method requires access to source model gradients (semi-black-box), which may not be available in all deployment settings.

## Evidence (verbatim from paper)

> Table 2: Restricted Data Setting: Toxicity Prediction

| Task | AMP Sequences Training Samples | R2DL Test Accuracy | Bi-LSTM Test Accuracy (train from scratch) |
| --- | --- | --- | --- |
| Toxicity Prediction | 5000 | 42.12 | 37.34 |
| Toxicity Prediction | 6000 | 62.98 | 49.62 |
| Toxicity Prediction | 7000 | 86.23 | 82.78 |
| Toxicity Prediction | 8153 | 89.34 | 93.7 |

## Citation

```bibtex
@misc{vinod2020reprogramming,
  title={Reprogramming Language Models for Molecular Representation Learning},
  author={Vinod et al. (2020)},
  year={2020},
  note={arXiv:2012.03460}
}
```

- arXiv: 2012.03460

---
name: ar-bench-eval
description: Evaluates large language models on appellate review tasks for criminal judgments, specifically detecting, classifying, and correcting legal errors in finalized court decisions. It probes fine-grained legal reasoning, diagnostic accuracy, and the ability to generate legally valid corrections. Use when the user wants to benchmark on AR-Bench, or asks about evaluating this task. Reports Accuracy (Acc), Macro F1 (MaF1).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.22742
  bibtex_key: li2026arbench
  confidence: high
---

# ar-bench-eval

> AR-BENCH: Benchmarking Legal Reasoning with Judgment Error Detection, Classification and Correction — Li et al. (2026) (arXiv:2601.22742, 2026)

## What this evaluates

Evaluates large language models on appellate review tasks for criminal judgments, specifically detecting, classifying, and correcting legal errors in finalized court decisions. It probes fine-grained legal reasoning, diagnostic accuracy, and the ability to generate legally valid corrections.

## Datasets

- **AR-Bench** — total 8700; splits: test (-1)

## Metrics

- `Accuracy (Acc)` **(primary)** — range: [0, 1]
  - Proportion of correctly predicted instances out of the total. For regression tasks (e.g., prison terms, fines), accuracy is computed within a specified tolerance (e.g., 0.1).
- `Macro F1 (MaF1)` **(primary)** — range: [0, 1]
  - Unweighted mean of F1 scores across all classes. Computed as 2 * (Precision * Recall) / (Precision + Recall) per class, then averaged. Preferred for imbalanced legal charge distributions.
- `Macro Precision (MaP)` — range: [0, 1]
  - Unweighted mean of precision scores across all classes. Precision is the ratio of true positives to all predicted positives per class.
- `Macro Recall (MaR)` — range: [0, 1]
  - Unweighted mean of recall scores across all classes. Recall is the ratio of true positives to all actual positives per class.

## Input / output format

**Input**: Case facts, anomalous judgment text, reasoning process, and cited law articles (varies by experimental setting S1–S5).

**Output**: For error detection: binary/class label indicating presence of error. For error classification: fine-grained error type category. For error correction: corrected judgment text or revised legal reasoning.

## Scoring recipe

```python
def compute_metrics(predictions, gold_labels):
    acc = sum(p == g for p, g in zip(predictions, gold_labels)) / len(gold_labels)
    classes = set(gold_labels) | set(predictions)
    f1_scores = []
    for c in classes:
        tp = sum(1 for p, g in zip(predictions, gold_labels) if p == c and g == c)
        fp = sum(1 for p, g in zip(predictions, gold_labels) if p == c and g != c)
        fn = sum(1 for p, g in zip(predictions, gold_labels) if p != c and g == c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1_scores.append(f1)
    macro_f1 = sum(f1_scores) / len(f1_scores)
    return acc, macro_f1
```

## Common pitfalls

- Naive inclusion of full legal statutes as additional context can introduce noise and degrade model performance compared to using only reasoning processes or case facts.
- Interval-based classification for correction tasks may obscure meaningful differences, as overlapping interval boundaries or overly broad thresholds can mask actual prediction errors.
- Simple Accuracy can be misleading due to imbalanced legal charge distributions; Macro-F1 is explicitly recommended as a more meaningful metric for rare and error-prone cases.

## Evidence (verbatim from paper)

> Therefore, Macro-F1 (MaF1) is a more meaningful evaluation metric in this setting. The relatively low MaF1 scores indicate both the challenging nature of our dataset and the limitations of current models in handling rare and error-prone cases.

## Citation

```bibtex
@misc{li2026arbench,
  title={AR-BENCH: Benchmarking Legal Reasoning with Judgment Error Detection, Classification and Correction},
  author={Li et al. (2026)},
  year={2026},
  note={arXiv:2601.22742}
}
```

- arXiv: 2601.22742

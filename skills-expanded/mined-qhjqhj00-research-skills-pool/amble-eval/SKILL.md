---
name: amble-eval
description: Evaluates archival domain adaptation capabilities across four distinct tasks. It probes a model's ability to predict document retention periods, classify open access status, determine confidentiality levels, and correct post-OCR text errors in Chinese archival records. Use when the user wants to benchmark on AMBLE, or asks about evaluating this task. Reports F1 score, Levenshtein Distance.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2307.14852
  bibtex_key: zhang2023arcgpt
  confidence: high
---

# amble-eval

> ArcGPT: A Large Language Model Tailored for Real-world Archival Applications — Zhang et al. (2023) (arXiv:2307.14852, 2023)

## What this evaluates

Evaluates archival domain adaptation capabilities across four distinct tasks. It probes a model's ability to predict document retention periods, classify open access status, determine confidentiality levels, and correct post-OCR text errors in Chinese archival records.

## Datasets

- **AMBLE** — total ?; splits: test (-1)

## Metrics

- `precision` — range: [0, 1]
  - Ratio of correctly predicted positive instances to the total predicted positives.
- `recall` — range: [0, 1]
  - Ratio of correctly predicted positive instances to the total actual positives.
- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall: 2 * (precision * recall) / (precision + recall).
- `Levenshtein Distance` **(primary)** — range: other
  - Minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another.

## Input / output format

**Input**: Archival record metadata (title, author, year, record ID) concatenated with OCR text, followed by a task-specific prompt (e.g., single-choice question for classification or raw text for OCR correction).

**Output**: For classification tasks: a single option label (A or B). For post-OCR processing: the corrected Chinese text.

## Scoring recipe

```python
def score_classification(preds, golds):
    tp = fp = fn = 0
    for p, g in zip(preds, golds):
        if p == g == 'positive': tp += 1
        elif p == 'positive' and g != 'positive': fp += 1
        elif p != 'positive' and g == 'positive': fn += 1
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    return {'precision': prec, 'recall': rec, 'f1': f1}

def score_ocr(preds, golds):
    return {'levenshtein_distance': sum(levenshtein(p, g) for p, g in zip(preds, golds)) / len(preds)}
```

## Common pitfalls

- The paper notes a performance gap between generative models (like ArcGPT) and predictive models (like RoBERTa), which may skew comparisons if not accounted for.
- Post-OCR evaluation uses Levenshtein Distance, which is sensitive to character-level errors in Chinese text and may not reflect semantic correctness.

## Evidence (verbatim from paper)

> To assess the overall performance of both baseline models and ArcGPT, we employed precision, recall, and F1 score as evaluation metrics. The results of these evaluations are presented in Table 2. Notably, ArcGPT demonstrated superior F1 scores of 84.40, 84.00, and 94.4 for open-access identification, retention period prediction, and confidentiality prediction, respectively.

## Citation

```bibtex
@misc{zhang2023arcgpt,
  title={ArcGPT: A Large Language Model Tailored for Real-world Archival Applications},
  author={Zhang et al. (2023)},
  year={2023},
  note={arXiv:2307.14852}
}
```

- arXiv: 2307.14852

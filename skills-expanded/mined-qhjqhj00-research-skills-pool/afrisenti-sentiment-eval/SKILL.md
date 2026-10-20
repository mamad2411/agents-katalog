---
name: afrisenti-sentiment-eval
description: Evaluates sentiment classification capabilities across 14 low-resource African languages using Twitter data. Tests both monolingual and multilingual transfer, as well as zero-shot adaptation via parameter-efficient fine-tuning. Use when the user wants to benchmark on AfriSenti, or asks about evaluating this task. Reports weighted F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.06459
  bibtex_key: azime2023masakhane
  confidence: high
---

# afrisenti-sentiment-eval

> Masakhane-Afrisenti at SemEval-2023 Task 12: Sentiment Analysis using Afro-centric Language Models and Adapters for Low-resource African Languages — Azime et al. (2023) (arXiv:2304.06459, 2023)

## What this evaluates

Evaluates sentiment classification capabilities across 14 low-resource African languages using Twitter data. Tests both monolingual and multilingual transfer, as well as zero-shot adaptation via parameter-efficient fine-tuning.

## Datasets

- **AfriSenti** — total ?; splits: train (-1), test (-1)

## Metrics

- `weighted F1 score` **(primary)** — range: [0, 1]
  - The weighted average of F1 scores across all sentiment classes, where each class's F1 is multiplied by its support (number of true instances) to account for class imbalance.

## Input / output format

**Input**: Raw text of Twitter posts in one of 14 African languages.

**Output**: Predicted sentiment label (e.g., positive, negative, neutral).

## Scoring recipe

```python
def compute_weighted_f1(predictions, gold):
    classes = sorted(set(predictions) | set(gold))
    f1s = []
    for c in classes:
        tp = sum(1 for p, g in zip(predictions, gold) if p == c and g == c)
        fp = sum(1 for p, g in zip(predictions, gold) if p == c and g != c)
        fn = sum(1 for p, g in zip(predictions, gold) if p != c and g == c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1s.append((f1, sum(1 for g in gold if g == c)))
    total_support = sum(s for _, s in f1s)
    return sum(f * s / total_support for f, s in f1s)
```

## Common pitfalls

- Dataset is highly imbalanced across languages, especially when combined for multilingual training.
- Label-based and language-based oversampling did not yield significant improvements, so balancing strategies should be used cautiously.
- Development set lacks labels and must be treated as a held-out test set for internal model selection.

## Evidence (verbatim from paper)

> We utilized a weighted F1 score as the evaluation metric for our models. The training dataset was originally from the AfriSenti dataset, which is a corpus of 14 African languages scraped from Twitter for sentiment analysis tasks.

## Citation

```bibtex
@misc{azime2023masakhane,
  title={Masakhane-Afrisenti at SemEval-2023 Task 12: Sentiment Analysis using Afro-centric Language Models and Adapters for Low-resource African Languages},
  author={Azime et al. (2023)},
  year={2023},
  note={arXiv:2304.06459}
}
```

- arXiv: 2304.06459

---
name: afrisenti-eval
description: Evaluates multilingual and cross-lingual sentiment classification capabilities on low-resource African languages using Twitter data. It probes how well pre-trained language models handle dialectal variation, code-switching, and mixed scripts in fine-tuning and zero-shot transfer settings. Use when the user wants to benchmark on AfriSenti, or asks about evaluating this task. Reports F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2302.08956
  bibtex_key: shamsuddeen2023afrisenti
  confidence: high
---

# afrisenti-eval

> AfriSenti: A Twitter Sentiment Analysis Benchmark for African Languages — Shamsuddeen Hassan Muhammad et al. (2023) (arXiv:2302.08956, 2023)

## What this evaluates

Evaluates multilingual and cross-lingual sentiment classification capabilities on low-resource African languages using Twitter data. It probes how well pre-trained language models handle dialectal variation, code-switching, and mixed scripts in fine-tuning and zero-shot transfer settings.

## Datasets

- **AfriSenti** — total ?; splits: train (-1), test (-1); repo https://github.com/afrisenti-semeval/afrisent-semeval-2023

## Metrics

- `F1` **(primary)** — range: percent
  - Macro-averaged F1 score across sentiment classes. Computed as the harmonic mean of precision and recall per class, then averaged across all classes.

## Input / output format

**Input**: Raw tweet text in one of 14 African languages.

**Output**: Predicted sentiment label (positive, negative, or neutral).

## Scoring recipe

```python
def compute_f1(predictions, gold):
    classes = sorted(set(predictions + gold))
    f1_scores = []
    for cls in classes:
        tp = sum(1 for p, g in zip(predictions, gold) if p == cls and g == cls)
        fp = sum(1 for p, g in zip(predictions, gold) if p == cls and g != cls)
        fn = sum(1 for p, g in zip(predictions, gold) if p != cls and g == cls)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1_scores.append(f1)
    return sum(f1_scores) / len(f1_scores) * 100
```

## Common pitfalls

- Zero-shot transfer is only evaluated on Oromo (orm) and Tigrinya (tir), so results do not generalize to other low-resource African languages.
- F1 scores are reported as percentages in tables (e.g., 71.2), but internal calculations may use a 0-1 scale; ensure consistent scaling when reproducing.
- Models are fine-tuned for exactly 10 epochs with fixed learning rates (2e-5 or 1e-5); deviating from this schedule will break reproducibility.

## Evidence (verbatim from paper)

> We used a standard configuration for text classification fine-tuning on HuggingFace with a learning rate of $2e-5$ for smaller PLMs and $1e-5$ for larger PLMs, a batch size of 128, and 10 epochs. Table 7 shows the results of the monolingual baseline models on AfriSenti. XLM-T performs particularly well on Arabic and Portuguese dialects, i.e., arq, ary and pt-MZ, where it outperforms AfriBERTa by 21.8, 14.2, and 13.0 and AfroXLMR-base by 4.0, 5.9, and 4.7 F1 points respectively.

## Citation

```bibtex
@misc{shamsuddeen2023afrisenti,
  title={AfriSenti: A Twitter Sentiment Analysis Benchmark for African Languages},
  author={Shamsuddeen Hassan Muhammad et al. (2023)},
  year={2023},
  note={arXiv:2302.08956}
}
```

- arXiv: 2302.08956

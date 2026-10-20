---
name: aste-triplet-extraction-eval
description: Evaluates a model's ability to jointly extract aspect terms, opinion terms, and their sentiment polarities from text. It probes fine-grained aspect-based sentiment analysis by requiring precise span detection and correct pairing of components within sentences. Use when the user wants to benchmark on 14res, 14lap, 15res, 16res, or asks about evaluating this task. Reports F score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1911.01616
  bibtex_key: peng2019knowing
  confidence: high
---

# aste-triplet-extraction-eval

> Knowing What, How and Why: A Near Complete Solution for Aspect-based Sentiment Analysis — Peng et al. (2019) (arXiv:1911.01616, 2019)

## What this evaluates

Evaluates a model's ability to jointly extract aspect terms, opinion terms, and their sentiment polarities from text. It probes fine-grained aspect-based sentiment analysis by requiring precise span detection and correct pairing of components within sentences.

## Datasets

- **14res** — total ?; splits: train (1300), valid (323), test (496); repo https://github.com/xuuuluuu/SemEval-Triplet-data
- **14lap** — total ?; splits: train (920), valid (228), test (339); repo https://github.com/xuuuluuu/SemEval-Triplet-data
- **15res** — total ?; splits: train (593), valid (148), test (318); repo https://github.com/xuuuluuu/SemEval-Triplet-data
- **16res** — total ?; splits: train (842), valid (210), test (320); repo https://github.com/xuuuluuu/SemEval-Triplet-data

## Metrics

- `F score` **(primary)** — range: percent
  - Harmonic mean of precision and recall for exact triplet or pair matches. F = 2 * (P * R) / (P + R).
- `Precision` — range: percent
  - Ratio of correctly predicted triplets/pairs to all predicted triplets/pairs.
- `Recall` — range: percent
  - Ratio of correctly predicted triplets/pairs to all ground-truth triplets/pairs.

## Input / output format

**Input**: Raw sentence string.

**Output**: A list of triplets formatted as (aspect_term, opinion_term, sentiment_polarity) or pairs formatted as (aspect_term, opinion_term).

## Scoring recipe

```python
def compute_f1(preds, gold):
    pred_set = set(preds)
    gold_set = set(gold)
    tp = len(pred_set & gold_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1
```

## Common pitfalls

- Cascaded evaluation: Stage-two triplet/pair metrics are computed by stacking the stage-two classifier on top of stage-one baselines, meaning errors from aspect/opinion extraction propagate and inflate false positives/negatives.
- Pairing ambiguity: Sentences with multiple co-occurring aspects and opinions require explicit pairing logic; naive distance-based or greedy pairing often yields incorrect associations without contextual classifiers.
- Tagging scheme confusion: The paper uses a unified tagging scheme (e.g., T-POS, S) for training, but evaluation is done on extracted spans; misinterpreting the BIO vs. unified tag format can lead to incorrect span extraction.

## Evidence (verbatim from paper)

> In terms of F score, our core model has again achieved the best performance compared with all existing baselines. Li-unified-R is generally not as good as our model on the restaurant datasets, but still performs very competitive and event better than our model on 14lap.

## Citation

```bibtex
@misc{peng2019knowing,
  title={Knowing What, How and Why: A Near Complete Solution for Aspect-based Sentiment Analysis},
  author={Peng et al. (2019)},
  year={2019},
  note={arXiv:1911.01616}
}
```

- arXiv: 1911.01616

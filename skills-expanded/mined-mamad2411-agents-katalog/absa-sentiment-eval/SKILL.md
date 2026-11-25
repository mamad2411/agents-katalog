---
name: absa-sentiment-eval
description: Probes an LLM's ability to identify granular sentiment toward specific topics within a text, including custom labels like 'not mentioned' and 'wished for'. It tests fine-grained aspect-level classification rather than overall review sentiment. Use when the user wants to benchmark on TravelBench ABSA, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.02719
  bibtex_key: billa2025travelbench
  confidence: high
---

# absa-sentiment-eval

> TravelBench : Exploring LLM Performance in Low-Resource Domains — Billa et al. (2025) (arXiv:2510.02719, 2025)

## What this evaluates

Probes an LLM's ability to identify granular sentiment toward specific topics within a text, including custom labels like 'not mentioned' and 'wished for'. It tests fine-grained aspect-level classification rather than overall review sentiment.

## Datasets

- **TravelBench ABSA** — total ?; splits: test (-1)

## Metrics

- `F1-score` **(primary)** — range: [0, 1]
  - Computes the F1-score between prediction and ground truth labels using the Van Rijsbergen formulation.

## Input / output format

**Input**: A hotel review text and a pre-defined set of topics (e.g., WiFi, pool, parking).

**Output**: Sentiment label per aspect: positive, negative, mixed, neutral, not mentioned, or wished for.

## Scoring recipe

```python
def compute_f1(predictions, golds):
    tp = sum(1 for p, g in zip(predictions, golds) if p == g)
    fp = sum(1 for p, g in zip(predictions, golds) if p != g and p in golds)
    fn = sum(1 for p, g in zip(predictions, golds) if p != g and g not in predictions)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    return 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
```

## Common pitfalls

- Custom labels 'not mentioned' and 'wished for' are often missed by models trained on standard sentiment datasets.
- Aspect-level granularity requires aligning predictions with specific topics, not just overall review sentiment.

## Evidence (verbatim from paper)

> We compute the F1-score Van Rijsbergen ([1979])* between prediction and ground truth for evaluation.

## Citation

```bibtex
@misc{billa2025travelbench,
  title={TravelBench : Exploring LLM Performance in Low-Resource Domains},
  author={Billa et al. (2025)},
  year={2025},
  note={arXiv:2510.02719}
}
```

- arXiv: 2510.02719

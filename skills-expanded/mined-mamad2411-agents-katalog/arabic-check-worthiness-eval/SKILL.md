---
name: arabic-check-worthiness-eval
description: This benchmark evaluates a model's ability to identify check-worthy factual claims within Arabic social media posts. It probes the system's capacity to filter out non-factual or irrelevant content and prioritize claims that require verification based on public interest and potential impact. Use when the user wants to benchmark on Arabic Check-Worthiness Dataset, or asks about evaluating this task. Reports P@30.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.07997
  bibtex_key: barroncedeno2020checkthat
  confidence: high
---

# arabic-check-worthiness-eval

> Overview of CheckThat! 2020: Automatic Identification and Verification of Claims in Social Media — Barrón-Cedeno et al. (2020) (arXiv:2007.07997, 2020)

## What this evaluates

This benchmark evaluates a model's ability to identify check-worthy factual claims within Arabic social media posts. It probes the system's capacity to filter out non-factual or irrelevant content and prioritize claims that require verification based on public interest and potential impact.

## Datasets

- **Arabic Check-Worthiness Dataset** — total 7500; splits: train (1500), test (6000)

## Metrics

- `P@30` **(primary)** — range: [0, 1]
  - Precision at cutoff k=30, measuring the proportion of check-worthy tweets among the top 30 ranked results.
- `MAP` — range: [0, 1]
  - Mean Average Precision, averaging the precision values at each rank where a check-worthy tweet appears.

## Input / output format

**Input**: Arabic tweet text.

**Output**: Binary label (check-worthy / not check-worthy) or a ranked list of tweets.

## Scoring recipe

```python
def score(predictions, gold):
    top_k = predictions[:30]
    relevant_in_top_k = len(set(top_k) & gold)
    return relevant_in_top_k / 30.0
```

## Common pitfalls

- Check-worthiness is subjective; annotators used a 4-question scale to resolve disagreements, but the final label is binary.
- The dataset is topic-stratified: 3 topics for training, 12 for testing, so models must generalize across unseen topics.

## Evidence (verbatim from paper)

> We evaluated the runs using precision at k (P@k) and Mean Average Precision (MAP). We considered P@30 as the official measure, as we anticipated the user would check maximum of 30 claims per week.

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

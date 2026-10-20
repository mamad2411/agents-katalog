---
name: authorship-attribution-eval
description: Evaluates a model's ability to identify an author from their writing style while suppressing domain-specific (fandom) style leakage. It probes cross-domain generalization and robustness to domain swapping in binary authorship attribution. Use when the user wants to benchmark on Fanfiction Corpus, or asks about evaluating this task. Reports mean macro accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2005.14714
  bibtex_key: bischoff2020importance
  confidence: high
---

# authorship-attribution-eval

> The Importance of Suppressing Domain Style in Authorship Analysis — Bischoff et al. (2020) (arXiv:2005.14714, 2020)

## What this evaluates

Evaluates a model's ability to identify an author from their writing style while suppressing domain-specific (fandom) style leakage. It probes cross-domain generalization and robustness to domain swapping in binary authorship attribution.

## Datasets

- **Fanfiction Corpus** — total ?; splits: train (-1), test (-1)

## Metrics

- `mean macro accuracy` **(primary)** — range: percent
  - Macro-averaged accuracy computed across all problem instances (author pairs and fandom combinations). For binary classification, this is equivalent to the proportion of correctly predicted author labels averaged over at least ten repetitions per instance.

## Input / output format

**Input**: Text chunks of up to 500 tokens, represented as character trigrams or learned embeddings.

**Output**: Binary author label prediction (e.g., Author A or Author B).

## Scoring recipe

```python
def compute_macro_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)

# Final metric is the mean of compute_macro_accuracy across >=10 repetitions
```

## Common pitfalls

- High accuracy in traditional same-domain setups often reflects domain style exploitation rather than true author style capture.
- Models must be evaluated on equal text lengths (max 500 tokens) to ensure fairness across different learning paradigms.
- Domain swapping experiments require careful balancing of training data to allow adversarial training without zero-knowledge constraints.

## Evidence (verbatim from paper)

> As performance measure, we employ the mean macro accuracy over at least ten problem instances for every experiment.

## Citation

```bibtex
@misc{bischoff2020importance,
  title={The Importance of Suppressing Domain Style in Authorship Analysis},
  author={Bischoff et al. (2020)},
  year={2020},
  note={arXiv:2005.14714}
}
```

- arXiv: 2005.14714

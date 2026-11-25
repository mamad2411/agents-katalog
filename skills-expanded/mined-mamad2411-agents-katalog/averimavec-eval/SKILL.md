---
name: averimavec-eval
description: This benchmark probes a model's ability to perform multimodal fact-checking by verifying real-world image-text claims. It requires the system to retrieve cross-modal evidence, analyze inconsistencies, and produce a justified verdict that aligns with ground truth labels. Use when the user wants to benchmark on AVerImaTeC, or asks about evaluating this task. Reports verdict_correctness.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.04587
  bibtex_key: jung2026verifying
  confidence: high
---

# averimavec-eval

> VILLAIN at AVerImaTeC: Verifying Image-Text Claims via Multi-Agent Collaboration — Jung et al. (2026) (arXiv:2602.04587, 2026)

## What this evaluates

This benchmark probes a model's ability to perform multimodal fact-checking by verifying real-world image-text claims. It requires the system to retrieve cross-modal evidence, analyze inconsistencies, and produce a justified verdict that aligns with ground truth labels.

## Datasets

- **AVerImaTeC** — total ?; splits: test (-1)

## Metrics

- `verdict_correctness` **(primary)** — range: [0, 1]
  - A response is correct only if the predicted label matches the ground truth AND the provided evidence score meets or exceeds a threshold of λ=0.3.

## Input / output format

**Input**: Image-text claim along with its associated metadata.

**Output**: Predicted verdict label and supporting evidence.

## Scoring recipe

```python
def score(predictions, gold):
    correct = 0
    for pred, gold_label, pred_evidence in zip(predictions, gold['labels'], gold['evidence']):
        label_ok = (pred['label'] == gold_label)
        evidence_ok = pred['evidence_score'] >= 0.3
        if label_ok and evidence_ok:
            correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- A correct label alone is insufficient; the evidence score must also meet the λ=0.3 threshold.
- Evidence can be retrieved from multiple sources (web, document collections, or image collections), not just the web.

## Evidence (verbatim from paper)

> A response is considered correct only if both the predicted label is correct and the provided evidence is adequate. Specifically, a verdict is deemed correct only when the evidence score meets or exceeds the threshold $\lambda=0.3$.

## Citation

```bibtex
@misc{jung2026verifying,
  title={VILLAIN at AVerImaTeC: Verifying Image-Text Claims via Multi-Agent Collaboration},
  author={Jung et al. (2026)},
  year={2026},
  note={arXiv:2602.04587}
}
```

- arXiv: 2602.04587

---
name: ancholik-ner-eval
description: Evaluates Named Entity Recognition (NER) capabilities across five regional dialects of the Bangla language. It probes a model's ability to correctly identify and classify entities (Person, Location, Organization, Role, Food) in dialect-specific text where linguistic features and vocabulary differ significantly from standard Bangla. Use when the user wants to benchmark on ANCHOLIK-NER, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2502.11198
  bibtex_key: paul2025ancholikner
  confidence: high
---

# ancholik-ner-eval

> ANCHOLIK-NER: A Benchmark Dataset for Bangla Regional Named Entity Recognition — Paul et al. (2025) (arXiv:2502.11198, 2025)

## What this evaluates

Evaluates Named Entity Recognition (NER) capabilities across five regional dialects of the Bangla language. It probes a model's ability to correctly identify and classify entities (Person, Location, Organization, Role, Food) in dialect-specific text where linguistic features and vocabulary differ significantly from standard Bangla.

## Datasets

- **ANCHOLIK-NER** — total 17405; splits: test (-1)

## Metrics

- `F1-score` **(primary)** — range: percent
  - Harmonic mean of precision and recall: F1 = 2 * (Precision * Recall) / (Precision + Recall). Precision is the ratio of correctly predicted positive entities to all predicted positives, and recall is the ratio of correctly predicted positives to all actual positives.

## Input / output format

**Input**: Sentences written in regional Bangla dialects (Barishal, Chittagong, Mymensingh, Noakhali, Sylhet) containing named entities to be identified.

**Output**: Token-level or span-level entity labels (e.g., PER, LOC, ORG, ROLE, FOOD) corresponding to the input text.

## Scoring recipe

```python
def compute_f1(predictions, gold):
    tp = sum(1 for p, g in zip(predictions, gold) if p == g and p != 'O')
    fp = sum(1 for p, g in zip(predictions, gold) if p != g and p != 'O')
    fn = sum(1 for p, g in zip(predictions, gold) if p != g and g != 'O')
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return f1
```

## Common pitfalls

- Dialect-specific vocabulary and syntax cause significant drops in precision and recall, particularly for the Chittagong region.
- Models frequently confuse Role (ROLE) and Organization (ORG) entities, leading to high false positive rates across all regions.

## Evidence (verbatim from paper)

> The performance of three different BERT models—Bangla BERT, Bangla BERT Base, and BERT Base Multilingual Cased—was evaluated for Named Entity Recognition (NER) across five regional dialects of Bangla: Barishal, Chittagong, Mymensingh, Noakhali, and Sylhet. The models were trained with a particular learning rates (2e-5), different batch sizes (8, 16) and epochs(5, 10, 15, 20). Their performance was assessed based on precision, recall, and F1-score.

## Citation

```bibtex
@misc{paul2025ancholikner,
  title={ANCHOLIK-NER: A Benchmark Dataset for Bangla Regional Named Entity Recognition},
  author={Paul et al. (2025)},
  year={2025},
  note={arXiv:2502.11198}
}
```

- arXiv: 2502.11198

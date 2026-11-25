---
name: auslaw-citation-eval
description: Evaluates an LLM's ability to predict the correct legal citation for a given query text. It probes the model's capacity to retrieve or generate accurate references from a large Australian legal corpus, testing both retrieval and generation capabilities in a domain-specific setting. Use when the user wants to benchmark on AusLaw Citation Benchmark, or asks about evaluating this task. Reports ACC@1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.06272
  bibtex_key: han2024auslawcitation
  confidence: high
---

# auslaw-citation-eval

> Evaluating LLM-based Approaches to Legal Citation Prediction: Domain-specific Pre-training, Fine-tuning, or RAG? A Benchmark and an Australian Law Case Study — Han et al. (2024) (arXiv:2412.06272, 2024)

## What this evaluates

Evaluates an LLM's ability to predict the correct legal citation for a given query text. It probes the model's capacity to retrieve or generate accurate references from a large Australian legal corpus, testing both retrieval and generation capabilities in a domain-specific setting.

## Datasets

- **AusLaw Citation Benchmark** — total 55000; splits: train (-1), test (-1)

## Metrics

- `ACC@1` **(primary)** — range: percent
  - The percentage of instances where the model's top-1 predicted citation exactly matches the ground-truth citation.
- `ACC@5` — range: percent
  - The percentage of instances where the ground-truth citation appears within the model's top-5 predicted citations.

## Input / output format

**Input**: Query text, optionally augmented with RoC (Rules of Court) or RoC Aggregations.

**Output**: A ranked list of candidate citations (Top-5 or Top-1).

## Scoring recipe

```python
def compute_acc_at_k(predictions, gold, k):
    hits = sum(1 for pred in predictions[:k] if pred == gold)
    return (hits / len(gold)) * 100
```

## Common pitfalls

- Performance is heavily skewed by citation frequency; cases cited >100 times achieve ~100% accuracy, while those cited <20 times drop below 40%.
- Index granularity significantly impacts retrieval performance; RoC Aggregations outperform both Full Cases and Catchwords, contrary to initial expectations.
- Domain-specific pre-training alone is insufficient for accurate citation prediction; targeted instruction tuning is required to achieve competitive results.

## Evidence (verbatim from paper)

> As evaluation metrics, Accuracy@1 and Accuracy@5 are used.

## Citation

```bibtex
@misc{han2024auslawcitation,
  title={Evaluating LLM-based Approaches to Legal Citation Prediction: Domain-specific Pre-training, Fine-tuning, or RAG? A Benchmark and an Australian Law Case Study},
  author={Han et al. (2024)},
  year={2024},
  note={arXiv:2412.06272}
}
```

- arXiv: 2412.06272

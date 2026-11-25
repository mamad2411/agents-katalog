---
name: artistmus-eval
description: This benchmark evaluates the factual accuracy and contextual reasoning capabilities of LLMs in music question answering. It specifically probes how well models can retrieve and utilize artist-centric knowledge from a domain-specific database versus relying on parametric memory, comparing zero-shot, RAG, and reranked retrieval strategies. Use when the user wants to benchmark on ArtistMus, TrustMus, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.05430
  bibtex_key: kwon2025artistmus
  confidence: high
---

# artistmus-eval

> ArtistMus: A Globally Diverse, Artist-Centric Benchmark for Retrieval-Augmented Music Question Answering — Kwon et al. (2025) (arXiv:2512.05430, 2025)

## What this evaluates

This benchmark evaluates the factual accuracy and contextual reasoning capabilities of LLMs in music question answering. It specifically probes how well models can retrieve and utilize artist-centric knowledge from a domain-specific database versus relying on parametric memory, comparing zero-shot, RAG, and reranked retrieval strategies.

## Datasets

- **ArtistMus** — total 1000; splits: test (1000)
- **TrustMus** — total 500; splits: test (500)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Exact match between the model's predicted option (A, B, C, or D) and the ground-truth correct option. Calculated as the number of correct predictions divided by the total number of questions.

## Input / output format

**Input**: Multiple-choice question with four options (A, B, C, D). For RAG experiments, the input also includes retrieved passages from MusWikiDB (top-k based on retriever config and fixed 1024-token budget).

**Output**: A single letter corresponding to the chosen option (A, B, C, or D).

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    correct = 0
    for pred, gold in zip(predictions, golds):
        if pred.strip().upper() == gold.strip().upper():
            correct += 1
    return correct / len(golds)
```

## Common pitfalls

- Evaluation must be run with temperature=0 to ensure deterministic outputs, as non-deterministic sampling will break exact-match scoring.
- The RAG setup enforces a strict 1024-token budget for retrieved passages, requiring careful adjustment of top-k based on passage size (128, 256, or 512 tokens).
- Accuracy is defined strictly as exact match of the option letter, not semantic similarity or free-text generation.

## Evidence (verbatim from paper)

> All evaluations use a multiple-choice QA format, and accuracy (exact match of the predicted option A, B, C, or D) was adopted as the evaluation metric.

## Citation

```bibtex
@misc{kwon2025artistmus,
  title={ArtistMus: A Globally Diverse, Artist-Centric Benchmark for Retrieval-Augmented Music Question Answering},
  author={Kwon et al. (2025)},
  year={2025},
  note={arXiv:2512.05430}
}
```

- arXiv: 2512.05430

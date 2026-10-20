---
name: arabic-sts-mteb-eval
description: Evaluates the semantic textual similarity (STS) capability of Arabic text embedding models, specifically testing how Matryoshka Representation Learning and hybrid loss training preserve semantic alignment across different embedding dimensions. Use when the user wants to benchmark on MTEB Arabic STS (STS17, STS22, STS22-v2), or asks about evaluating this task. Reports STS correlation (Pearson/Spearman, scaled 0-100).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.24581
  bibtex_key: nacar2025gate
  confidence: high
---

# arabic-sts-mteb-eval

> GATE: General Arabic Text Embedding for Enhanced Semantic Textual Similarity with Matryoshka Representation Learning and Hybrid Loss Training — Nacar et al. (2025) (arXiv:2505.24581, 2025)

## What this evaluates

Evaluates the semantic textual similarity (STS) capability of Arabic text embedding models, specifically testing how Matryoshka Representation Learning and hybrid loss training preserve semantic alignment across different embedding dimensions.

## Datasets

- **MTEB Arabic STS (STS17, STS22, STS22-v2)** — total ?; splits: test (-1)

## Metrics

- `STS correlation (Pearson/Spearman, scaled 0-100)` **(primary)** — range: percent
  - Computes cosine or dot-product similarity between sentence embeddings, then calculates Pearson or Spearman correlation against ground truth labels (0–5 scale). Results are multiplied by 100 for reporting, following MTEB conventions.

## Input / output format

**Input**: Pairs of Arabic sentences.

**Output**: Continuous similarity scores (0.0–1.0) derived from embedding similarity, or directly the correlation score against ground truth.

## Scoring recipe

```python
def compute_sts_score(embeddings, ground_truth_labels):
    predicted_scores = cosine_similarity(embeddings)
    corr = pearsonr(predicted_scores, ground_truth_labels)[0]
    return corr * 100
```

## Common pitfalls

- The ground truth labels are on a 0–5 scale, but the reported metric is correlation scaled to 0–100; confusing these leads to misinterpretation of scores like 69.99.
- Matryoshka models are evaluated at multiple dimensions (768 down to 64); comparing only the largest dimension ignores the core efficiency claim of the framework.
- Cosine similarity is the standard for STS, but the paper also reports Dot Product, Manhattan, and Euclidean, which can yield different rankings for lower-dimensional embeddings.

## Evidence (verbatim from paper)

> To evaluate the effectiveness of Matryoshka and Multi-Task Hybrid Loss methods, we conduct experiments on GATE models, and their base counterparts using the Massive Text Embedding Benchmark (MTEB)*Muennighoff et al. ([2022])* for Arabic. MTEB provides a large-scale evaluation across various NLP tasks, including Semantic Textual Similarity (STS), with key Arabic metrics: STS17, STS22, and STS22-v2*Cer et al. ([2017])*. These metrics assess STS on a scale from 0 to 5, focusing on Arabic-Arabic sentence pairs.

## Citation

```bibtex
@misc{nacar2025gate,
  title={GATE: General Arabic Text Embedding for Enhanced Semantic Textual Similarity with Matryoshka Representation Learning and Hybrid Loss Training},
  author={Nacar et al. (2025)},
  year={2025},
  note={arXiv:2505.24581}
}
```

- arXiv: 2505.24581

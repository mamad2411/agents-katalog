---
name: armenian-embedding-benchmark-eval
description: Evaluates the semantic retrieval and similarity capabilities of text embedding models on low-resource Armenian text. It probes cross-lingual alignment, domain coverage, and robustness to noisy synthetic training data by measuring retrieval accuracy and semantic similarity correlation across diverse tasks. Use when the user wants to benchmark on MTEB [hye], Manual Retrieval Dataset, MS MARCO [hye], STS [hye], or asks about evaluating this task. Reports Average.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.22290
  bibtex_key: navasardyan2026less
  confidence: high
---

# armenian-embedding-benchmark-eval

> Less is More: Adapting Text Embeddings for Low-Resource Languages with Small Scale Noisy Synthetic Data — Navasardyan et al. (2026) (arXiv:2603.22290, 2026)

## What this evaluates

Evaluates the semantic retrieval and similarity capabilities of text embedding models on low-resource Armenian text. It probes cross-lingual alignment, domain coverage, and robustness to noisy synthetic training data by measuring retrieval accuracy and semantic similarity correlation across diverse tasks.

## Datasets

- **MTEB [hye]** — total ?; splits: test (-1)
- **Manual Retrieval Dataset** — total 185; splits: test (185)
- **MS MARCO [hye]** — total 10000; splits: val (10000)
- **STS [hye]** — total 3000; splits: test (3000)

## Metrics

- `Top-20 Accuracy` — range: percent
  - Percentage of queries where the ground-truth passage ranks within the top 20 retrieved results.
- `Spearman Correlation` — range: other
  - Rank-based correlation coefficient measuring the monotonic relationship between predicted similarity scores and human-annotated STS scores.
- `Top-10 Accuracy` — range: percent
  - Percentage of queries where the ground-truth passage ranks within the top 10 retrieved results.
- `Mean (Task)` — range: percent
  - Standard MTEB task-level average score across the 9 datasets and 5 tasks in the Armenian subset.
- `Average` **(primary)** — range: other
  - Simple arithmetic mean of the four benchmark scores: Top-20 Accuracy, Spearman Correlation, Top-10 Accuracy, and Mean (Task).

## Input / output format

**Input**: Armenian query and passage/document pairs for retrieval tasks, or sentence pairs for semantic textual similarity (STS) tasks.

**Output**: Embedding vectors for each text; retrieval rankings or similarity scores used to compute accuracy and correlation.

## Scoring recipe

```python
def compute_metrics(predictions, gold):
    top20_acc = top_k_accuracy(predictions['manual'], gold['manual'], k=20)
    top10_acc = top_k_accuracy(predictions['marco'], gold['marco'], k=10)
    sts_corr = spearman_correlation(predictions['sts'], gold['sts'])
    mteb_score = mean_task_score(predictions['mteb'], gold['mteb'])
    avg = (top20_acc + top10_acc + sts_corr + mteb_score) / 4
    return {'Top-20 Accuracy': top20_acc, 'Top-10 Accuracy': top10_acc,
            'Spearman Correlation': sts_corr, 'Mean (Task)': mteb_score, 'Average': avg}
```

## Common pitfalls

- Using the public English MS MARCO test set instead of the translated validation subset, which the authors explicitly note is not public.
- Assuming higher translation quality or larger dataset sizes linearly improve performance; the paper demonstrates early semantic saturation where noisy 10k pairs match or exceed 1M clean pairs.
- Overlooking the 'Merged' checkpoint results, which frequently outperform 'Main' checkpoints in retrieval tasks due to model averaging.

## Evidence (verbatim from paper)

> Metrics reported are Top-20 Accuracy for Retrieval, Spearman Correlation for STS, and Top-10 Accuracy for MS MARCO. We use standard Mean (Task) for MTEB as reported on their benchmark. We also report the average score across those 4 benchmarks.

## Citation

```bibtex
@misc{navasardyan2026less,
  title={Less is More: Adapting Text Embeddings for Low-Resource Languages with Small Scale Noisy Synthetic Data},
  author={Navasardyan et al. (2026)},
  year={2026},
  note={arXiv:2603.22290}
}
```

- arXiv: 2603.22290

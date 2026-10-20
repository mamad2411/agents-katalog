---
name: afrimteb-eval
description: Evaluates text embedding models on a wide range of African language tasks, including classification, retrieval, semantic similarity, clustering, and bitext mining. It probes cross-lingual transfer, language coverage, and the ability of embeddings to capture semantic and discriminative signals across 59 African languages. Use when the user wants to benchmark on AfriMTEB, AfriMTEB-Lite, or asks about evaluating this task. Reports macro average score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.23896
  bibtex_key: uemura2025afrimteb
  confidence: high
---

# afrimteb-eval

> AfriMTEB and AfriE5: Benchmarking and Adapting Text Embedding Models for African Languages — Uemura et al. (2025) (arXiv:2510.23896, 2025)

## What this evaluates

Evaluates text embedding models on a wide range of African language tasks, including classification, retrieval, semantic similarity, clustering, and bitext mining. It probes cross-lingual transfer, language coverage, and the ability of embeddings to capture semantic and discriminative signals across 59 African languages.

## Datasets

- **AfriMTEB** — total ?; splits: test (-1)
- **AfriMTEB-Lite** — total ?; splits: test (-1)

## Metrics

- `macro average score` **(primary)** — range: percent
  - Macro-average of task-specific scores across all datasets in the benchmark. Task-specific scores are reported as percentages or points out of 100, covering classification, retrieval, semantic textual similarity, clustering, bitext mining, and reranking.

## Input / output format

**Input**: Text pairs, documents, or queries in African languages. For classification tasks, input text with corresponding labels; for retrieval/STS/reranking, input text pairs or query-document pairs.

**Output**: Text embeddings (for retrieval/STS/reranking) or predicted class labels/rankings (for classification tasks). Scores are aggregated into a macro-average percentage.

## Scoring recipe

```python
task_scores = []
for task in benchmark_tasks:
    task_scores.append(compute_task_metric(predictions[task], gold[task]))
macro_avg = sum(task_scores) / len(task_scores)
return macro_avg
```

## Common pitfalls

- Assuming larger model size (7B/8B) guarantees better performance; the paper shows smaller models with better language coverage outperform larger ones.
- Confusing AfriMTEB (59 languages, 38 datasets) with AfriMTEB-Lite (9 languages, 12 tasks); results differ significantly between the full suite and the lite subset.
- Expecting uniform gains across all task families; adaptation improves some tasks (e.g., classification, reranking) while slightly trading off others (e.g., bitext mining, STS).

## Evidence (verbatim from paper)

> AfriE5-Large-Instruct attains the best macro average at 62.4, edging out Gemini embedding (60.6) and mE5-Large-Instruct (61.3) in [Table 2].

## Citation

```bibtex
@misc{uemura2025afrimteb,
  title={AfriMTEB and AfriE5: Benchmarking and Adapting Text Embedding Models for African Languages},
  author={Uemura et al. (2025)},
  year={2025},
  note={arXiv:2510.23896}
}
```

- arXiv: 2510.23896

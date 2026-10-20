---
name: arabicmteb-eval
description: Evaluates Arabic-centric and cross-lingual text embedding models across multiple linguistic, cultural, and domain-specific capabilities. It probes how well models capture dialectal variations, regional cultural knowledge, and specialized domain terminology in Arabic. Use when the user wants to benchmark on ArabicMTEB, or asks about evaluating this task. Reports Avg..
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2411.01192
  bibtex_key: bhatia2024swan
  confidence: high
---

# arabicmteb-eval

> Swan and ArabicMTEB: Dialect-Aware, Arabic-Centric, Cross-Lingual, and Cross-Cultural Embedding Models and Benchmarks — Bhatia et al. (2024) (arXiv:2411.01192, 2024)

## What this evaluates

Evaluates Arabic-centric and cross-lingual text embedding models across multiple linguistic, cultural, and domain-specific capabilities. It probes how well models capture dialectal variations, regional cultural knowledge, and specialized domain terminology in Arabic.

## Datasets

- **ArabicMTEB** — total ?; splits: overall (-1), dialectal (-1), domain-specific (-1), cultural (-1)

## Metrics

- `Avg.` **(primary)** — range: [0, 100]
  - Macro-average of normalized scores across all evaluated tasks (RTR, STS, PairCLF, CLF, CLR, RRK, BTM). Each task score is scaled to a 0-100 range before averaging.
- `RTR` — range: [0, 100]
  - Mean Reciprocal Rank or NDCG@K for Arabic retrieval tasks, measuring how well the model ranks relevant documents for a given query.
- `STS` — range: [0, 100]
  - Pearson or Spearman correlation between cosine similarities of predicted embeddings and human-assigned semantic similarity scores.
- `CLF` — range: [0, 100]
  - Classification accuracy or F1 score for document or sentence classification tasks.

## Input / output format

**Input**: Query-document pairs for retrieval, sentence pairs for similarity/classification, and document collections for clustering.

**Output**: Fixed-dimensional embedding vectors (e.g., 768 or 4096 dimensions) for each input text.

## Scoring recipe

```python
def compute_avg_score(task_scores):
    valid_tasks = ['RTR', 'STS', 'PairCLF', 'CLF', 'CLR', 'RRK', 'BTM']
    scores = [task_scores[t] for t in valid_tasks if t in task_scores]
    return sum(scores) / len(scores) if scores else 0.0

def score_task(predictions, gold, task_type):
    if task_type == 'STS':
        return pearson_corr([cosine_sim(p, g) for p, g in zip(predictions, gold)], gold_labels) * 100
    elif task_type == 'RTR':
        return compute_mrr_or_ndcg(predictions, gold) * 100
    elif task_type == 'CLF':
        return accuracy(predictions, gold) * 100
    return 0.0
```

## Common pitfalls

- Failing to distinguish between Modern Standard Arabic (MSA) and dialectal performance, as models often score high on MSA but drop significantly on dialectal splits.
- Averaging raw task scores without normalizing them to a common scale (0-100), which skews the overall benchmark score due to differing metric ranges across tasks like retrieval vs. clustering.
- Ignoring cost-effectiveness metrics alongside accuracy, as the benchmark explicitly tracks inference cost per 10k documents to evaluate practical deployment viability.

## Evidence (verbatim from paper)

> In these tables, the tasks will be referred to as RTR: Retrieval, STS: Semantic Textual Similarity, PairCLF: Pair Classification, CLF: Classification, CLR: Clustering, RRK: Reranking, and BTM: BiText Mining.

## Citation

```bibtex
@misc{bhatia2024swan,
  title={Swan and ArabicMTEB: Dialect-Aware, Arabic-Centric, Cross-Lingual, and Cross-Cultural Embedding Models and Benchmarks},
  author={Bhatia et al. (2024)},
  year={2024},
  note={arXiv:2411.01192}
}
```

- arXiv: 2411.01192

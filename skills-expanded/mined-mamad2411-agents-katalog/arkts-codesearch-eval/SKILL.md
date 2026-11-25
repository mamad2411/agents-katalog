---
name: arkts-codesearch-eval
description: Evaluates code embedding models on a semantic code retrieval task where the goal is to find the correct ArkTS function given a natural language docstring or comment. It probes the model's ability to align bilingual documentation with declarative UI and distributed application code semantics. Use when the user wants to benchmark on ArkTS-CodeSearch, or asks about evaluating this task. Reports MRR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.05550
  bibtex_key: he2026arktscodesearch
  confidence: high
---

# arkts-codesearch-eval

> ArkTS-CodeSearch: A Open-Source ArkTS Dataset for Code Retrieval — He et al. (2026) (arXiv:2602.05550, 2026)

## What this evaluates

Evaluates code embedding models on a semantic code retrieval task where the goal is to find the correct ArkTS function given a natural language docstring or comment. It probes the model's ability to align bilingual documentation with declarative UI and distributed application code semantics.

## Datasets

- **ArkTS-CodeSearch** — total ?; splits: train (-1), test (-1)

## Metrics

- `MRR` **(primary)** — range: [0, 1]
  - Mean Reciprocal Rank: the average of the reciprocal ranks of the first relevant document across all queries. Calculated as 1/rank where rank is the position of the first correct function in the retrieved list.
- `NDCG@5` — range: [0, 1]
  - Normalized Discounted Cumulative Gain at cutoff 5. Measures the quality of the top-5 ranked results by applying a logarithmic discount to the relevance score at each position, normalized by the ideal ranking.
- `Recall@1` — range: [0, 1]
  - Binary indicator of whether the single most relevant function appears at the top of the retrieved list.
- `Recall@5` — range: [0, 1]
  - Proportion of relevant functions found within the top-5 retrieved results, averaged across queries.

## Input / output format

**Input**: Natural language docstring or comment describing an ArkTS function.

**Output**: A ranked list of ArkTS functions (or function identifiers) retrieved by the embedding model, evaluated at top-1 and top-5 positions.

## Scoring recipe

```python
def compute_metrics(retrieved_ids, relevant_ids):
    rank = next((i+1 for i, rid in enumerate(retrieved_ids) if rid in relevant_ids), len(retrieved_ids)+1)
    mrr = 1.0 / rank
    recall_at_1 = 1.0 if retrieved_ids[0] in relevant_ids else 0.0
    recall_at_5 = len(set(retrieved_ids[:5]) & relevant_ids) / len(relevant_ids)
    # NDCG@5 uses standard log2(rank+1) discounting over top-5
    return mrr, recall_at_1, recall_at_5
```

## Common pitfalls

- Assuming off-the-shelf general-purpose sentence embedding models will perform well without domain-specific fine-tuning, as they often suffer from language and domain mismatch with ArkTS documentation.
- Overlooking the impact of bilingual (Chinese/English) docstrings, which significantly favors models pretrained on Chinese corpora over purely English ones.
- Confusing zero-shot baseline performance with fine-tuned performance, as the paper shows substantial gains and ranking shifts after supervised contrastive learning.

## Evidence (verbatim from paper)

> We report results on the held-out test set using standard information retrieval metrics, including Mean Reciprocal Rank (MRR), NDCG@5, and Recall@K.

## Citation

```bibtex
@misc{he2026arktscodesearch,
  title={ArkTS-CodeSearch: A Open-Source ArkTS Dataset for Code Retrieval},
  author={He et al. (2026)},
  year={2026},
  note={arXiv:2602.05550}
}
```

- arXiv: 2602.05550

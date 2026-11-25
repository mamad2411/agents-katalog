---
name: astronomical-semantic-search-eval
description: Evaluates zero-shot semantic retrieval of astronomical images using natural language queries, specifically probing the model's ability to identify rare galactic phenomena (spirals, mergers, gravitational lenses) without curated training labels. It also measures the impact of VLM-based re-ranking on retrieval precision for rare classes. Use when the user wants to benchmark on HSC survey galaxy images, or asks about evaluating this task. Reports nDCG@10.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.11982
  bibtex_key: koblischke2025semantic
  confidence: high
---

# astronomical-semantic-search-eval

> Semantic search for 100M+ galaxy images using AI-generated captions — Koblischke et al. (2025) (arXiv:2512.11982, 2025)

## What this evaluates

Evaluates zero-shot semantic retrieval of astronomical images using natural language queries, specifically probing the model's ability to identify rare galactic phenomena (spirals, mergers, gravitational lenses) without curated training labels. It also measures the impact of VLM-based re-ranking on retrieval precision for rare classes.

## Datasets

- **HSC survey galaxy images** — total ?; splits: test (-1); repo https://github.com/NolanKoblischke/AION-Search

## Metrics

- `nDCG@10` **(primary)** — range: [0, 1]
  - Normalized Discounted Cumulative Gain at rank 10. DCG@10 = sum_{i=1}^{10} (rel_i / log2(i+1)), divided by the ideal DCG@10 computed from ground-truth relevance labels sorted in descending order. Values range from 0 to 1, with 1 indicating perfect ranking.

## Input / output format

**Input**: Free-form natural language query describing an astronomical phenomenon (e.g., 'visible spiral arms', 'merging', 'gravitational lens') paired against a large unlabeled image archive.

**Output**: Ranked list of retrieved images (top-10 for primary metric computation, top-1000 for re-ranking evaluation).

## Scoring recipe

```python
def compute_ndcg_at_10(relevance_scores, top_k=10):
    dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(relevance_scores[:top_k]))
    ideal_rels = sorted(relevance_scores, reverse=True)[:top_k]
    idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal_rels))
    return dcg / idcg if idcg > 0 else 0.0

# Applied per query, then averaged across all queries for each category
```

## Common pitfalls

- Evaluating only the initial zero-shot retrieval without applying the GPT-4.1 re-ranking stage, which the paper notes nearly doubles recall for rare phenomena like gravitational lenses.
- Comparing semantic search results against supervised similarity baselines without noting that baselines were trained on single-sentence summaries while the proposed method uses VLM-generated captions, making direct performance gaps partially attributable to caption quality.
- Assuming the 200-lens test set size applies to all categories; spiral and merger test set sizes are unstated in the text.

## Evidence (verbatim from paper)

> Table 1 reports nDCG@10 scores for retrieval for spiral galaxies, mergers, and gravitational lenses. Our AION-Search model, trained on the summarized VLM-generated captions, consistently outperforms similarity-based baselines across all categories. For spirals, we observe an nDCG@10 of 0.941 compared to 0.643 for the strongest baseline (AION-1-L). For mergers, the model achieves 0.554 versus 0.384 (AION-1-XL), and for gravitational lenses 0.180 compared to 0.015 (AION-1-XL).

## Citation

```bibtex
@misc{koblischke2025semantic,
  title={Semantic search for 100M+ galaxy images using AI-generated captions},
  author={Koblischke et al. (2025)},
  year={2025},
  note={arXiv:2512.11982}
}
```

- arXiv: 2512.11982

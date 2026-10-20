---
name: 3d-shape-retrieval-eval
description: Evaluates algorithms for retrieving geometrically and topologically similar 3D shapes from a database given a query shape. Probes pose invariance, shape descriptor robustness, and retrieval ranking accuracy. Use when the user wants to benchmark on NIST shape benchmark, or asks about evaluating this task. Reports precision-recall.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1105.3685
  bibtex_key: godil2011benchmarks
  confidence: medium
---

# 3d-shape-retrieval-eval

> Benchmarks, Performance Evaluation and Contests for 3D Shape Retrieval — Godil et al. (2011) (arXiv:1105.3685, 2011)

## What this evaluates

Evaluates algorithms for retrieving geometrically and topologically similar 3D shapes from a database given a query shape. Probes pose invariance, shape descriptor robustness, and retrieval ranking accuracy.

## Datasets

- **NIST shape benchmark** — total ?; splits: test (-1)

## Metrics

- `precision-recall` **(primary)** — range: [0, 1]
  - Computes precision and recall at various recall levels to plot a PR curve, summarizing retrieval performance across different thresholds.
- `R-precision` — range: [0, 1]
  - The precision at rank R, where R is the total number of relevant items in the database. Calculated as the number of relevant items retrieved in the top R results divided by R.
- `average precision` — range: [0, 1]
  - The mean of precision values computed at each rank where a relevant item is retrieved, averaged over all queries.

## Input / output format

**Input**: A query 3D shape model (typically pose-normalized for rotation, translation, and scale invariance) and a target database of 3D models.

**Output**: A ranked list of database models ordered by similarity score to the query shape.

## Scoring recipe

```python
def compute_r_precision(retrieved_top_r, relevant_set):
    hits = len(set(retrieved_top_r) & relevant_set)
    return hits / len(relevant_set)

def compute_average_precision(retrieved_list, relevant_set):
    hits = 0
    sum_prec = 0.0
    for i, model_id in enumerate(retrieved_list, 1):
        if model_id in relevant_set:
            hits += 1
            sum_prec += hits / i
    return sum_prec / len(relevant_set) if relevant_set else 0.0
```

## Common pitfalls

- Failing to apply pose normalization (rotation, translation, scale) before feature extraction, leading to false negatives.
- Mesh errors in web-crawled models can distort geometric similarity scores if not pre-processed.
- Manual ground truth classification requires multiple assessors and a tiebreaker to ensure stability and reduce subjective bias.

## Evidence (verbatim from paper)

> The paper introduces standardized evaluation measures—precision-recall, R-precision, and average precision—applied across SHREC contest tracks, emphasizing the importance of geometric and topological similarity in ground truth labeling and the need for invariant, scalable, and publicly accessible datasets.

## Citation

```bibtex
@misc{godil2011benchmarks,
  title={Benchmarks, Performance Evaluation and Contests for 3D Shape Retrieval},
  author={Godil et al. (2011)},
  year={2011},
  note={arXiv:1105.3685}
}
```

- arXiv: 1105.3685

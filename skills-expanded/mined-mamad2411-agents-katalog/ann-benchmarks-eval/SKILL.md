---
name: ann-benchmarks-eval
description: This benchmark evaluates approximate nearest neighbor (ANN) search algorithms by measuring the trade-off between search quality (recall) and computational efficiency (queries per second, index size, and build time). It probes how well different algorithmic families perform across diverse high-dimensional datasets and distance metrics, revealing robustness and approximation capabilities. Use when the user wants to benchmark on SIFT, GIST, GLOVE, NYTimes, Rand-Euclidean, SIFT-Hamming, Word2Bits, or asks about evaluating this task. Reports recall.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1807.05614
  bibtex_key: aumuller2018annbenchmarks
  confidence: high
---

# ann-benchmarks-eval

> ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms — Aumüller et al. (2018) (arXiv:1807.05614, 2018)

## What this evaluates

This benchmark evaluates approximate nearest neighbor (ANN) search algorithms by measuring the trade-off between search quality (recall) and computational efficiency (queries per second, index size, and build time). It probes how well different algorithmic families perform across diverse high-dimensional datasets and distance metrics, revealing robustness and approximation capabilities.

## Datasets

- **SIFT** — total 1000000; splits: test (-1)
- **GIST** — total 1000000; splits: test (-1)
- **GLOVE** — total 1183514; splits: test (-1)
- **NYTimes** — total 234791; splits: test (-1)
- **Rand-Euclidean** — total 1000000; splits: test (-1)
- **SIFT-Hamming** — total 1000000; splits: test (-1)
- **Word2Bits** — total 399000; splits: test (-1)

## Metrics

- `recall` **(primary)** — range: [0, 1]
  - The fraction of true k-nearest neighbors that appear in the algorithm's returned top-k candidates. Calculated as |predictions ∩ true_knn| / k.
- `QPS` — range: other
  - Queries Per Second, measuring throughput. Calculated as the total number of queries executed divided by the total wall-clock time spent answering them.

## Input / output format

**Input**: A dataset of high-dimensional vectors, a query vector, a distance metric (Euclidean, Cosine, or Hamming), and an integer k specifying the number of nearest neighbors to retrieve.

**Output**: A ranked list of k candidate vectors (or their indices) from the dataset, plus the constructed index structure used for search.

## Scoring recipe

```python
def compute_recall(predictions, true_knn, k):
    return len(set(predictions) & set(true_knn)) / k

def compute_qps(num_queries, total_query_time_seconds):
    return num_queries / total_query_time_seconds

# Combined metric used in paper:
# index_size_scaled = index_size_kb / qps
```

## Common pitfalls

- Most algorithms do not accept recall as a direct input parameter, requiring extensive manual tuning of internal hyperparameters to hit target recall levels.
- A strict 5-hour time limit for index construction prevents some algorithms (e.g., FLANN, HNSW at high recall) from completing auto-tuning or building optimal indexes, skewing high-recall comparisons.
- The combined 'index size scaled by QPS' metric can mask raw speed or memory trade-offs, making it easy to misinterpret performance if only one axis is considered.

## Evidence (verbatim from paper)

> Figure 4 shows the relationship between an algorithm’s achieved recall and the number of queries it can answer per second (its QPS) on the two datasets GLOVE (Cosine similarity) and SIFT (Euclidean distance) for 10- and 100-nearest neighbor queries.

## Citation

```bibtex
@misc{aumuller2018annbenchmarks,
  title={ANN-Benchmarks: A Benchmarking Tool for Approximate Nearest Neighbor Algorithms},
  author={Aumüller et al. (2018)},
  year={2018},
  note={arXiv:1807.05614}
}
```

- arXiv: 1807.05614

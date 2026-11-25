---
name: attrgau-eval
description: Evaluates session-based recommendation models enhanced with the AttrGAU framework on their ability to predict the next item in a user session. It probes robustness to data sparsity and noisy interactions, and measures the model-agnostic performance gain over vanilla backbones. Use when the user wants to benchmark on Dressipi, Diginetica, Retailrocket, or asks about evaluating this task. Reports HR@N, MRR@N.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.10296
  bibtex_key: zhao2024attrgau
  confidence: high
---

# attrgau-eval

> Enhancing Attributed Graph Networks with Alignment and Uniformity Constraints for Session-based Recommendation — Zhao et al. (2024) (arXiv:2410.10296, 2024)

## What this evaluates

Evaluates session-based recommendation models enhanced with the AttrGAU framework on their ability to predict the next item in a user session. It probes robustness to data sparsity and noisy interactions, and measures the model-agnostic performance gain over vanilla backbones.

## Datasets

- **Dressipi** — total ?; splits: train (-1), test (-1); repo https://www.recsyschallenge.com/2022/dataset.html
- **Diginetica** — total ?; splits: train (-1), test (-1); repo https://competitions.codalab.org/competitions/11161
- **Retailrocket** — total ?; splits: train (-1), test (-1); repo https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

## Metrics

- `HR@N` **(primary)** — range: percent
  - Hit Rate at rank N. Measures the proportion of test instances where the ground truth item appears in the top-N predicted items.
- `MRR@N` **(primary)** — range: percent
  - Mean Reciprocal Rank at rank N. Computes the average of the reciprocal of the rank of the first correct item in the top-N list (1/rank if correct, else 0).

## Input / output format

**Input**: A session sequence of item IDs $[v_{s,1}, ..., v_{s,n-1}]$ and the corresponding ground truth next item $v_{s,n}$.

**Output**: A ranked list of candidate items, or top-N predictions.

## Scoring recipe

```python
def compute_metrics(predictions, ground_truth, top_k=10):
    hits = 0
    mrr_sum = 0.0
    for pred_list, gt in zip(predictions, ground_truth):
        top_k_list = pred_list[:top_k]
        if gt in top_k_list:
            hits += 1
            rank = top_k_list.index(gt) + 1
            mrr_sum += 1.0 / rank
    hr = hits / len(ground_truth)
    mrr = mrr_sum / len(ground_truth)
    return hr, mrr
```

## Common pitfalls

- Session construction differs by dataset: Dressipi and Diginetica treat behaviors with the same session ID as one session, while Retailrocket splits continuous user behaviors within a 30-minute window.
- Test sets are constructed temporally (most recent one month/week/days), not randomly split, which affects reproducibility if timestamps are missing.
- Metrics are only reported at N=5 and N=10; other cutoffs are not evaluated.

## Evidence (verbatim from paper)

> We adopt two commonly used metrics for performance evaluation, i.e., Hit Rate (HR@N) and Mean Reciprocal Rank (MRR@N). Specifically, the former measures the proportion of the ground truth item in an unranked list, while the latter further considers the position of the ground truth item in a ranked list. And the larger the values the better the recommendation performance for both of them. In our experiments, we report the results of N=5,10.

## Citation

```bibtex
@misc{zhao2024attrgau,
  title={Enhancing Attributed Graph Networks with Alignment and Uniformity Constraints for Session-based Recommendation},
  author={Zhao et al. (2024)},
  year={2024},
  note={arXiv:2410.10296}
}
```

- arXiv: 2410.10296

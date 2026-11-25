---
name: agentds-eval
description: This benchmark evaluates AI agents and human-AI collaboration on domain-specific data science tasks across six industries. It probes the ability to perform feature engineering, integrate multimodal data (images, text, PDFs, JSON), and build predictive models that require genuine domain reasoning rather than generic pipelines. Use when the user wants to benchmark on AgentDS, or asks about evaluating this task. Reports quantile_score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.19005
  bibtex_key: luo2026agentds
  confidence: high
---

# agentds-eval

> AgentDS Technical Report: Benchmarking the Future of Human-AI Collaboration in Domain-Specific Data Science — An Luo et al. (2026) (arXiv:2603.19005, 2026)

## What this evaluates

This benchmark evaluates AI agents and human-AI collaboration on domain-specific data science tasks across six industries. It probes the ability to perform feature engineering, integrate multimodal data (images, text, PDFs, JSON), and build predictive models that require genuine domain reasoning rather than generic pipelines.

## Datasets

- **AgentDS** — total ?; splits: train (-1), test (-1)

## Metrics

- `quantile_score` **(primary)** — range: [0, 1]
  - Normalizes challenge-specific metric performance into a common [0, 1] scale based on participant ranking: q_i = (n - r_i) / (n - 1), where n is the number of participants and r_i is the rank (1=best). Non-submissions score 0.
- `macro_f1` — range: [0, 1]
  - Unweighted mean of recall for each class, used for classification challenges.
- `rmse` — range: other
  - Root mean squared error for regression challenges.
- `ndcg@10` — range: [0, 1]
  - Normalized discounted cumulative gain at rank 10 for ranking challenges.
- `mae` — range: other
  - Mean absolute error for regression challenges.
- `normalized_gini` — range: [0, 1]
  - Gini coefficient normalized by the perfect model's Gini, used for risk pricing and cost prediction.
- `mse` — range: other
  - Mean squared error for delay forecasting.

## Input / output format

**Input**: Challenge directory containing primary tabular training/test datasets, additional modalities (images, PDFs, JSON, CSV, text), and a description.md file detailing schema, prediction task, and submission format.

**Output**: A valid submission.csv file containing model predictions for the held-out test set.

## Scoring recipe

```python
def compute_quantile_score(metric_value, all_metric_values, higher_is_better=True):
    sorted_values = sorted(all_metric_values, reverse=higher_is_better)
    rank = sorted_values.index(metric_value) + 1
    n = len(sorted_values)
    if n <= 1:
        return 0.0
    return (n - rank) / (n - 1)
# Note: rank 1 is best performance. Non-submissions score 0.
```

## Common pitfalls

- Non-participation or failed submissions automatically receive a score of 0, which can drastically lower domain and overall averages.
- The quantile score is relative to the participant pool; absolute metric values do not directly translate to the final benchmark score.
- Ties in the overall score are broken first by submission count (fewer is better), then by submission timestamp (earlier is better).
- Generic modeling pipelines without domain-specific feature engineering or multimodal integration will underperform significantly.

## Evidence (verbatim from paper)

> Quantile scoring. To enable fair comparison across challenges with heterogeneous metrics and scales, AgentDS employs a quantile-based scoring that normalizes performance into a common [0, 1] scale. For each challenge, participants who submit solutions are ranked according to the challenge-specific metric (e.g., Macro-F1, RMSE, normalized Gini coefficient). Let i be the index of a participant who successfully submitted to the challenge, and let n>1 denote the number of such participants. The quantile score of participant i is computed as: q_i = (n - r_i) / (n - 1), where r_i denotes the rank of participant i (with r_i=1 indicating the best performance).

## Citation

```bibtex
@misc{luo2026agentds,
  title={AgentDS Technical Report: Benchmarking the Future of Human-AI Collaboration in Domain-Specific Data Science},
  author={An Luo et al. (2026)},
  year={2026},
  note={arXiv:2603.19005}
}
```

- arXiv: 2603.19005

---
name: average_per_token_log_prob
description: Evaluates language models on multiple-choice or candidate-selection downstream tasks by scoring candidate answers based on their likelihood under the model. It measures how well the model assigns high probability to the correct answer among a set of options. Use when the user has predictions and gold and needs to compute average_per_token_log_prob.
metadata:
  skill_kind: metric
  source_arxiv: 2507.19741
  bibtex_key: zhou2025basicreadingdistillation
  confidence: medium
---

# average_per_token_log_prob

> Basic Reading Distillation — Zhou et al. (2025) (arXiv:2507.19741, 2025)

## What this evaluates

Evaluates language models on multiple-choice or candidate-selection downstream tasks by scoring candidate answers based on their likelihood under the model. It measures how well the model assigns high probability to the correct answer among a set of options.

## Datasets

- **BIG-bench** — total ?; splits: test (-1); repo https://github.com/google/BIG-bench

## Metrics

- `average_per_token_log_prob` **(primary)** — range: other
  - Average of per-token log-probabilities of candidate answers: $\bar{P} = \frac{1}{n}\sum_{i=1}^{n}\log P_{i}(y_{i}|x_{\rm prompt})$, where $n$ is the number of words in the candidate answer $y$ and $x_{\rm prompt}$ is the input prompt.

## Input / output format

**Input**: A task prompt $x_{\rm prompt}$ and a list of candidate answers $y$.

**Output**: The candidate answer $y$ that maximizes the average per-token log-probability score.

## Scoring recipe

```python
def compute_avg_log_prob(prompt, candidate):
    tokens = candidate.split()
    n = len(tokens)
    log_probs = [model.log_prob(t, context=prompt) for t in tokens]
    return sum(log_probs) / n

def select_best_answer(prompt, candidates):
    scores = {c: compute_avg_log_prob(prompt, c) for c in candidates}
    return max(scores, key=scores.get)
```

## Common pitfalls

- Assumes a closed set of candidate answers is provided, making it unsuitable for open-ended generation tasks.
- Averaging log-probabilities per token can inadvertently favor shorter candidates if tokenization granularity or vocabulary coverage differs across options.
- Relies on downstream task prompts that are not standardized in the excerpt, potentially causing evaluation inconsistency across benchmarks.

## Evidence (verbatim from paper)

> For predicting the answers of the downstream tasks when testing the student model, we use the average of per-token log-probabilities of candidate answers as the scoring function for all downstream tasks: $\bar{P}=\frac{1}{n}\sum_{i=1}^{n}\log P_{i}(y_{i}|x_{\rm prompt})$ where $x_{\rm prompt}$ denotes the input to the student model, $y$ denotes the candidate answer for $x_{\rm prompt}$, and $n$ is the total number of words in $y$. We select $y$ with the maximal $\bar{P}$ as the final answer for $x_{\rm prompt}$.

## Citation

```bibtex
@misc{zhou2025basicreadingdistillation,
  title={Basic Reading Distillation},
  author={Zhou et al. (2025)},
  year={2025},
  note={arXiv:2507.19741}
}
```

- arXiv: 2507.19741

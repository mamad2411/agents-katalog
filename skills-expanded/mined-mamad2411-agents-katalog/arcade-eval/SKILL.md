---
name: arcade-eval
description: Evaluates large language models' ability to generate correct Python code for interactive data science notebooks, requiring multi-turn reasoning, grounded understanding of DataFrame schemas, and composition of pandas API calls based on preceding notebook context and natural language intents. Use when the user wants to benchmark on ARCADE, or asks about evaluating this task. Reports pass@k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2212.09248
  bibtex_key: yin2022arcade
  confidence: high
---

# arcade-eval

> Natural Language to Code Generation in Interactive Data Science Notebooks — Yin et al. (2022) (arXiv:2212.09248, 2022)

## What this evaluates

Evaluates large language models' ability to generate correct Python code for interactive data science notebooks, requiring multi-turn reasoning, grounded understanding of DataFrame schemas, and composition of pandas API calls based on preceding notebook context and natural language intents.

## Datasets

- **ARCADE** — total 1082; splits: Existing Tasks (-1), New Tasks (-1)

## Metrics

- `pass@k` **(primary)** — range: [0, 1]
  - The fraction of problems with at least one correct sample given a sample size k. Estimated by drawing 50 samples per problem to reduce variance.

## Input / output format

**Input**: Preceding notebook cells (code and comments), natural language intent for the current cell, NL description of DataFrame schema (columns and example values), and reference solutions to previous problems in multi-turn settings.

**Output**: Python code snippet to complete the current notebook cell.

## Scoring recipe

```python
def compute_pass_at_k(predictions_per_problem, k):
    # predictions_per_problem: list of k generated code strings
    # gold: reference solution or test suite (implied by pass@k convention)
    correct = any(is_correct(pred, gold) for pred in predictions_per_problem)
    return 1.0 if correct else 0.0

# Average over all problems to get pass@k
pass_at_k_score = sum(compute_pass_at_k(probs, k) for probs in all_problems) / len(all_problems)
```

## Common pitfalls

- Omitting the NL schema description from prompts causes significant performance drops, especially on the New Tasks split.
- Using only the immediate intent without preceding notebook context cells leads to failures in variable reference and state tracking.
- Existing Tasks scores may be inflated due to potential data leakage from popular GitHub notebooks into model training data.

## Evidence (verbatim from paper)

> Following prior work (Chen et al., 2021a; Austin et al., 2021), we measure model performance using the pass@k metric, defined as the fraction of problems with at least one correct sample given a sample size k. To reduce variance, we estimate pass@k (k ≤ 30) by drawing 50 samples for each problem (Chen et al., 2021a).

## Citation

```bibtex
@misc{yin2022arcade,
  title={Natural Language to Code Generation in Interactive Data Science Notebooks},
  author={Yin et al. (2022)},
  year={2022},
  note={arXiv:2212.09248}
}
```

- arXiv: 2212.09248

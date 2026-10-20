---
name: alphacode-eval
description: Evaluates a model's ability to generate correct, executable code for competitive programming problems under strict submission limits. It probes algorithmic reasoning, code synthesis, and the capacity to pass hidden test cases after filtering on provided examples. Use when the user wants to benchmark on CodeContests, or asks about evaluating this task. Reports solve rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2203.07814
  bibtex_key: li2022alphacode
  confidence: high
---

# alphacode-eval

> Competition-Level Code Generation with AlphaCode — Li et al. (2022) (arXiv:2203.07814, 2022)

## What this evaluates

Evaluates a model's ability to generate correct, executable code for competitive programming problems under strict submission limits. It probes algorithmic reasoning, code synthesis, and the capacity to pass hidden test cases after filtering on provided examples.

## Datasets

- **CodeContests** — total ?; splits: test (-1); repo https://github.com/deepmind/code_contests

## Metrics

- `solve rate` **(primary)** — range: percent
  - The percentage of problems for which at least one of the 10 allowed submissions passes the hidden test cases. Calculated as (number of solved problems / total problems) * 100.

## Input / output format

**Input**: Natural language problem description, optionally prefixed with metadata (rating, tags, language constraint) as a flat sequence of characters.

**Output**: A complete program in Python or C++ that reads input and prints output, generated autoregressively until an end-of-code token.

## Scoring recipe

```python
def compute_solve_rate(predictions, gold):
    solved_count = 0
    for problem in predictions:
        candidates = problem['filtered_samples']  # max 10 after clustering
        passed = False
        for code in candidates:
            if execute_and_check(code, problem['hidden_tests']):
                passed = True
                break
        if passed:
            solved_count += 1
    return (solved_count / len(predictions)) * 100
```

## Common pitfalls

- The 10-submission limit is strict; generating more samples does not improve the final score unless filtered down to 10.
- Filtering relies on example tests, which historically have high false-positive rates (30-60%) unless the dataset uses a strict temporal split to prevent data leakage.
- Clustering uses generated test inputs that may be invalid, but the protocol still groups programs by output behavior to avoid submitting semantically redundant solutions.

## Evidence (verbatim from paper)

> To accurately represent competitive programming contests and penalties, our formulation limits us to just 10 submissions per problem no matter how many samples we draw. One powerful tool for selecting these submissions is filtering samples to only those that pass the example tests given in the problem statement. ... AlphaCode achieves top 54.3% ranking in simulated Codeforces competitions by combining large-scale transformer models with extensive sampling and behavior-based filtering.

## Citation

```bibtex
@misc{li2022alphacode,
  title={Competition-Level Code Generation with AlphaCode},
  author={Li et al. (2022)},
  year={2022},
  note={arXiv:2203.07814}
}
```

- arXiv: 2203.07814

---
name: apps-eval
description: Evaluates a model's ability to generate correct Python code from natural language problem descriptions. It measures functional correctness by executing generated programs against a large bank of automated test cases, rather than relying on text-similarity metrics like BLEU. Use when the user wants to benchmark on APPS, or asks about evaluating this task. Reports strict_accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2105.09938
  bibtex_key: hendrycks2021apps
  confidence: high
---

# apps-eval

> Measuring Coding Challenge Competence With APPS — Hendrycks et al. (2021) (arXiv:2105.09938, 2021)

## What this evaluates

Evaluates a model's ability to generate correct Python code from natural language problem descriptions. It measures functional correctness by executing generated programs against a large bank of automated test cases, rather than relying on text-similarity metrics like BLEU.

## Datasets

- **APPS** — total 10000; splits: test (-1); repo https://github.com/hendrycks/apps

## Metrics

- `test_case_average` — range: percent
  - Average fraction of test cases passed across all problems. Computed as (1/P) * Σ_p (1/C_p) * Σ_c 1{eval(code_p, x_{p,c}) = y_{p,c}}.
- `strict_accuracy` **(primary)** — range: percent
  - Percentage of problems where the generated code passes every single test case. Computed as (1/P) * Σ_p Π_c 1{eval(code_p, x_{p,c}) = y_{p,c}}.

## Input / output format

**Input**: Natural language problem statement, problem format (call-based or standard input), and optional starter code.

**Output**: Python code string representing the solution.

## Scoring recipe

```python
def score(predictions, test_cases):
    P = len(predictions)
    tc_passes, strict_passes = [], []
    for p in range(P):
        code = predictions[p]
        cases = test_cases[p]
        C = len(cases)
        passed = sum(1 for x, y in cases if eval(code, x) == y)
        tc_passes.append(passed / C)
        strict_passes.append(1.0 if passed == C else 0.0)
    return sum(tc_passes) / P, sum(strict_passes) / P
```

## Common pitfalls

- BLEU scores are frequently used as a proxy but are anticorrelated with actual correctness and can mislead model comparison.
- Syntax errors (e.g., formatting, indentation, or missing colons) cause immediate evaluation failure even if the underlying algorithm is correct.
- Models may memorize solutions from pretraining data rather than demonstrating genuine code synthesis capability.

## Evidence (verbatim from paper)

> We aggregate the generated code's performance on test cases with two metrics, "test case average" and "strict accuracy." ... Strict accuracy is then computed by taking the number of solutions passing every test case divided by the total number of exercises.

## Citation

```bibtex
@misc{hendrycks2021apps,
  title={Measuring Coding Challenge Competence With APPS},
  author={Hendrycks et al. (2021)},
  year={2021},
  note={arXiv:2105.09938}
}
```

- arXiv: 2105.09938

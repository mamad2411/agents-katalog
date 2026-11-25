---
name: babelcode-eval
description: Evaluates the capability of large language models to generate executable code and translate code across multiple programming languages. It measures functional correctness by executing generated programs against test cases and computing the probability that at least one sample passes. Use when the user wants to benchmark on BC-HumanEval, BC-MBPP, BC-Transcoder, TP3, or asks about evaluating this task. Reports pass@k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2302.01973
  bibtex_key: orlanski2023measuring
  confidence: high
---

# babelcode-eval

> Measuring The Impact Of Programming Language Distribution — Orlanski et al. (2023) (arXiv:2302.01973, 2023)

## What this evaluates

Evaluates the capability of large language models to generate executable code and translate code across multiple programming languages. It measures functional correctness by executing generated programs against test cases and computing the probability that at least one sample passes.

## Datasets

- **BC-HumanEval** — total 161; splits: test (161)
- **BC-MBPP** — total 855; splits: test (855)
- **BC-Transcoder** — total 524; splits: test (524)
- **TP3** — total 370; splits: test (370)

## Metrics

- `pass@k` **(primary)** — range: [0, 1]
  - Estimates the probability that at least one of k sampled programs is correct. Computed as 1 - (binom(N - k, n_correct) / binom(N, n_correct)), averaged over all problems, where N is the total number of generated samples per problem and n_correct is the number of passing samples.

## Input / output format

**Input**: Zero-shot prompt containing the problem description and function signature. For translation tasks, the prompt includes the translated function signature without the docstring.

**Output**: Generated source code implementing the function.

## Scoring recipe

```python
import math
def pass_at_k(n_correct, k, N):
    if N - k < 0: return 0.0
    return 1.0 - math.comb(N - k, n_correct) / math.comb(N, n_correct)

# Per problem:
# N = 200 for generation tasks, N = 50 for translation tasks
# k = 100 for generation, k = 25 for translation
# Generate N samples, execute each against test cases, count n_correct
# Metric = mean(pass_at_k(n_correct, k, N) for all problems)
```

## Common pitfalls

- Using different sampling hyperparameters (T=0.8, top_p=0.95) than specified will significantly alter pass@k results.
- Confusing the total number of generated samples (N) with k, which directly changes the pass@k calculation denominator.
- Failing to execute code in the correct language-specific environment for each dataset, leading to false negatives.

## Evidence (verbatim from paper)

> We use the pass@k estimator (Chen et al., 2021) to measure the performance. We use k = 100 and k = 25 for generation and translation, respectively. For every dataset, we use T = 0.8, top_p = 0.95, and do not use top_k.

## Citation

```bibtex
@misc{orlanski2023measuring,
  title={Measuring The Impact Of Programming Language Distribution},
  author={Orlanski et al. (2023)},
  year={2023},
  note={arXiv:2302.01973}
}
```

- arXiv: 2302.01973

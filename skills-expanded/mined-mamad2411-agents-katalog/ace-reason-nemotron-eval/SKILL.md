---
name: ace-reason-nemotron-eval
description: This evaluation protocol assesses the mathematical reasoning and code generation capabilities of large language models. It probes the model's ability to solve competitive math problems and implement algorithms for coding contests under strict generation constraints. Use when the user wants to benchmark on AIME2024, AIME2025, MATH500, HMMT2025 Feb, BRUMO2025, LiveCodeBench v5, LiveCodeBench v6, Codeforces (LiveCodeBench Pro), EvalPlus, or asks about evaluating this task. Reports avg@k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.16400
  bibtex_key: chen2025acereasonnemotron
  confidence: high
---

# ace-reason-nemotron-eval

> AceReason-Nemotron: Advancing Math and Code Reasoning through Reinforcement Learning — Yang Chen et al. (2025) (arXiv:2505.16400, 2025)

## What this evaluates

This evaluation protocol assesses the mathematical reasoning and code generation capabilities of large language models. It probes the model's ability to solve competitive math problems and implement algorithms for coding contests under strict generation constraints.

## Datasets

- **AIME2024** — total ?; splits: test (-1)
- **AIME2025** — total ?; splits: test (-1)
- **MATH500** — total 500; splits: test (500)
- **HMMT2025 Feb** — total ?; splits: test (-1)
- **BRUMO2025** — total ?; splits: test (-1)
- **LiveCodeBench v5** — total ?; splits: test (-1)
- **LiveCodeBench v6** — total ?; splits: test (-1)
- **Codeforces (LiveCodeBench Pro)** — total ?; splits: test (-1)
- **EvalPlus** — total ?; splits: test (-1)

## Metrics

- `avg@k` **(primary)** — range: [0, 1]
  - The fraction of problems where at least one of the k sampled responses is correct. Calculated as pass@1 averaged over k generations to account for sampling variance in reasoning models.
- `Codeforces ELO` — range: other
  - Standard ELO rating derived from model performance on Codeforces problems via LiveCodeBench Pro.

## Input / output format

**Input**: Natural language math competition problems or coding problem statements (e.g., from AtCoder, LeetCode, Codeforces) with associated test cases or expected outputs.

**Output**: A reasoning trace followed by a final answer or code implementation, generated with temperature=0.6, top_p=0.95, and a maximum length of 32768 tokens.

## Scoring recipe

```python
def compute_avg_k(problems, k=64, temp=0.6, top_p=0.95, max_len=32768):
    correct = 0
    for prob in problems:
        samples = generate(prob, k, temp, top_p, max_len)
        if any(check_correctness(sample, prob.gold) for sample in samples):
            correct += 1
    return correct / len(problems)
```

## Common pitfalls

- Using k < 64 for small-scale benchmarks like AIME causes high standard error and unreliable pass@k estimates.
- Failing to strictly enforce temperature=0.6, top_p=0.95, and max_length=32768 leads to non-reproducible results across different runs.
- Mixing self-reported leaderboard numbers with independently evaluated results without checking the †/‡ markers in the paper.

## Evidence (verbatim from paper)

> Due to the high variance in outputs from reasoning models when using sampling, we report pass@1 performance averaged over k generations (avg@k). For small-scale benchmarks such as AIME, we use k=64, following DeepSeek-R1. This choice of k is critical for obtaining a reliable evaluation, as lower values of k lead to a significantly higher standard error of the mean (e.g., on AIME2024 @16/32/64: 1.8/1.2/0.7).

## Citation

```bibtex
@misc{chen2025acereasonnemotron,
  title={AceReason-Nemotron: Advancing Math and Code Reasoning through Reinforcement Learning},
  author={Yang Chen et al. (2025)},
  year={2025},
  note={arXiv:2505.16400}
}
```

- arXiv: 2505.16400

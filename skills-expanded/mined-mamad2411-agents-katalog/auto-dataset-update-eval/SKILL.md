---
name: auto-dataset-update-eval
description: Evaluates LLMs on automatically updated benchmark datasets (BIG-bench, MMLU) to measure evaluation stability, data leakage mitigation, and cognitive-level difficulty control via mimicking and extending generation strategies. Use when the user wants to benchmark on BIG-bench, MMLU, or asks about evaluating this task. Reports full-mark rate (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.11894
  bibtex_key: ying2024automating
  confidence: high
---

# auto-dataset-update-eval

> Automating Dataset Updates Towards Reliable and Timely Evaluation of Large Language Models — Ying et al. (2024) (arXiv:2402.11894, 2024)

## What this evaluates

Evaluates LLMs on automatically updated benchmark datasets (BIG-bench, MMLU) to measure evaluation stability, data leakage mitigation, and cognitive-level difficulty control via mimicking and extending generation strategies.

## Datasets

- **BIG-bench** — total ?; splits: test (-1)
- **MMLU** — total ?; splits: test (-1)

## Metrics

- `full-mark rate (%)` **(primary)** — range: percent
  - Percentage of correctly answered questions (full marks) on zero-shot evaluation. Calculated as (number of correct predictions / total number of samples) * 100.

## Input / output format

**Input**: Zero-shot prompts containing questions from benchmark datasets (BIG-bench, MMLU), including task descriptions and multiple-choice or open-ended queries.

**Output**: Model-generated answer or selected option.

## Scoring recipe

```python
def score(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p.strip().lower() == g.strip().lower())
    return (correct / len(gold)) * 100
```

## Common pitfalls

- Data leakage simulation involves fine-tuning on the original test set, which can artificially inflate performance if not properly controlled or reported.
- The mimicking strategy may inadvertently introduce external knowledge (e.g., periodic tables) that changes task difficulty compared to the original benchmark.
- Cognitive levels in the extending strategy require careful prompt engineering to ensure samples actually match the intended Bloom's taxonomy level.

## Evidence (verbatim from paper)

> Table 7: Average percentage (%) of full-mark of the fine-tuned model on the extended dataset over the four iterations, and the standard deviation.

## Citation

```bibtex
@misc{ying2024automating,
  title={Automating Dataset Updates Towards Reliable and Timely Evaluation of Large Language Models},
  author={Ying et al. (2024)},
  year={2024},
  note={arXiv:2402.11894}
}
```

- arXiv: 2402.11894

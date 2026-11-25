---
name: aidabench-eval
description: Evaluates LLM-driven document analysis agents on end-to-end data analytics workflows, including question answering, data visualization, and file generation. It probes multi-step numerical reasoning, cross-data consistency, and long-horizon planning on heterogeneous real-world documents. Use when the user wants to benchmark on AIDABench, or asks about evaluating this task. Reports Pass@3.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.15636
  bibtex_key: yang2026aidabench
  confidence: high
---

# aidabench-eval

> AIDABench: AI Data Analytics Benchmark — Yang et al. (2026) (arXiv:2603.15636, 2026)

## What this evaluates

Evaluates LLM-driven document analysis agents on end-to-end data analytics workflows, including question answering, data visualization, and file generation. It probes multi-step numerical reasoning, cross-data consistency, and long-horizon planning on heterogeneous real-world documents.

## Datasets

- **AIDABench** — total 600; splits: Easy (-1), Medium (-1), Hard (-1); repo https://github.com/MichaelYang-lyx/AIDABench

## Metrics

- `Pass@3` **(primary)** — range: percent
  - Pass@k measures the probability that at least one of k generated attempts is correct. For Pass@3, the model is allowed up to 3 attempts per task, and the metric reports the percentage of tasks where at least one attempt passes the evaluation criteria.

## Input / output format

**Input**: Heterogeneous real-world documents (spreadsheets, databases, financial reports) with associated analytical questions or tasks requiring multi-step reasoning.

**Output**: Model-generated outputs including answers, data visualizations, or generated files, evaluated for correctness against expert-verified ground truth.

## Scoring recipe

```python
def pass_at_k(predictions, k=3):
    correct = [bool(p) for p in predictions]
    return 1.0 if any(correct) else 0.0

score = (sum(pass_at_k(task_preds) for task_preds in all_tasks) / total_tasks) * 100
```

## Common pitfalls

- Difficulty is defined strictly by operation-chain length (number of key expert steps), not by task type or domain.
- Pass@3 allows up to 3 attempts per task; reporting Pass@1 will significantly underestimate model capability.
- Tasks span three distinct dimensions (QA, visualization, file generation) but are aggregated in the main table, masking dimension-specific performance.

## Evidence (verbatim from paper)

> We stratify task difficulty by operation-chain length, defined as the number of key expert operations (Steps). Low complexity ( ≤ 6 ) accounts for 29.5% of tasks, medium (7-12) for 49.4%, and high ( ≥ 13 ) for 21.1% . Table 4 reports pass@3 performance on each split.

## Citation

```bibtex
@misc{yang2026aidabench,
  title={AIDABench: AI Data Analytics Benchmark},
  author={Yang et al. (2026)},
  year={2026},
  note={arXiv:2603.15636}
}
```

- arXiv: 2603.15636

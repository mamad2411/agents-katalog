---
name: agent-spec-eval
description: Evaluates the cross-framework portability and reusability of declarative agent specifications by executing identical agentic workflows across four different runtime frameworks (AutoGen, CrewAI, LangGraph, WayFlow) on three distinct task benchmarks. Use when the user wants to benchmark on SimpleQA Verified, BIRD-SQL, $\tau^{2}$-Bench, or asks about evaluating this task. Reports F1 score, EX%, Passˆk.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.04173
  bibtex_key: benajiba2025agentspec
  confidence: high
---

# agent-spec-eval

> Open Agent Specification (Agent Spec) Technical Report — Benajiba et al. (2025) (arXiv:2510.04173, 2025)

## What this evaluates

Evaluates the cross-framework portability and reusability of declarative agent specifications by executing identical agentic workflows across four different runtime frameworks (AutoGen, CrewAI, LangGraph, WayFlow) on three distinct task benchmarks.

## Datasets

- **SimpleQA Verified** — total 1000; splits: test (1000)
- **BIRD-SQL** — total 1534; splits: dev (1534)
- **$\tau^{2}$-Bench** — total ?; splits: test (-1)

## Metrics

- `F1 score` **(primary)** — range: percent
  - Exact-match F1 score calculated over verified answers for SimpleQA Verified.
- `EX%` **(primary)** — range: percent
  - Execution accuracy comparing the generated SQL query to the ground-truth SQL query for BIRD-SQL.
- `Passˆk` **(primary)** — range: percent
  - Probability that all k attempts are correct out of k total attempts for $	au^{2}$-Bench.

## Input / output format

**Input**: Benchmark query or task (e.g., question, natural language query, or user simulation prompt) passed to an Agent Spec JSON configuration that defines the agent's tools, control flow, and model routing.

**Output**: Model/tool execution traces and final answers or generated SQL queries, evaluated against ground-truth labels.

## Scoring recipe

```python
def compute_metrics(predictions, gold, k=1):
    # F1 / Exact Match
    f1 = sum(1 for p, g in zip(predictions, gold) if p.strip() == g.strip()) / len(gold)
    # Execution Accuracy (SQL)
    ex = sum(1 for p, g in zip(predictions, gold) if execute_sql(p) == execute_sql(g)) / len(gold)
    # Pass@k
    pass_k = sum(1 for attempts in predictions if all(a == g for a, g in zip(attempts, gold))) / len(gold)
    return {'F1': f1, 'EX%': ex, 'Pass@k': pass_k}
```

## Common pitfalls

- Framework-specific prompt wrapping and tool-calling differences significantly impact results, making direct performance comparisons sensitive to runtime implementation details rather than just agent design.
- Some frameworks (AutoGen, CrewAI) lack support for non-agentic flow execution, resulting in missing flow-based results for certain benchmarks.
- Using web-browsing tools simplifies SimpleQA, so scores reflect tool-augmented capability rather than pure model reasoning.

## Evidence (verbatim from paper)

> We report F1 scores for SimpleQA Verified (exact-match over verified answers), EX% for BIRD-SQL (execution accuracy for generated SQL compared to ground-truth SQL), and Passˆk for $	au^{2}$-Bench (probability to get all k attempts correct out of k). Query time is reported as mean ± standard deviation over all records.

## Citation

```bibtex
@misc{benajiba2025agentspec,
  title={Open Agent Specification (Agent Spec) Technical Report},
  author={Benajiba et al. (2025)},
  year={2025},
  note={arXiv:2510.04173}
}
```

- arXiv: 2510.04173

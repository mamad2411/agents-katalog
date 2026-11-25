---
name: art-eval
description: Probes medical AI agents' ability to perform action-based reasoning on synthetic EHR tasks, specifically targeting data retrieval, temporal aggregation, and threshold-based conditional logic. It measures how well models handle clinical failure modes like missing data, numerical aggregation, and constraint chaining. Use when the user wants to benchmark on ART, or asks about evaluating this task. Reports Success Rate (SR; exact match).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.08988
  bibtex_key: mantravadi2026art
  confidence: high
---

# art-eval

> ART: Action-based Reasoning Task Benchmarking for Medical AI Agents — Mantravadi et al. (2026) (arXiv:2601.08988, 2026)

## What this evaluates

Probes medical AI agents' ability to perform action-based reasoning on synthetic EHR tasks, specifically targeting data retrieval, temporal aggregation, and threshold-based conditional logic. It measures how well models handle clinical failure modes like missing data, numerical aggregation, and constraint chaining.

## Datasets

- **ART** — total 200; splits: test (200)

## Metrics

- `Success Rate (SR; exact match)` **(primary)** — range: percent
  - Calculated as the percentage of tasks answered correctly via exact match. Evaluated separately for three categories: data retrieval, aggregation, and threshold/conditional logic.

## Input / output format

**Input**: Synthetic clinical tasks derived from EHR data, requiring models to retrieve specific records, aggregate values over 24-hour temporal windows, or apply threshold/conditional logic to patient data.

**Output**: Exact match answer to the clinical task (binary success/failure or precise numerical/logical output as specified by the task prompt).

## Scoring recipe

```python
def calculate_sr(predictions, gold, category):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    total = len(predictions)
    return (correct / total) * 100 if total > 0 else 0
```

## Common pitfalls

- Models achieve near-perfect retrieval only when prompts explicitly specify sorting/ordering instructions (e.g., 'sort by date'), indicating high sensitivity to prompt phrasing.
- Temporal aggregation over 24-hour windows and multi-step threshold logic consistently cause sharp performance drops, revealing limitations in constraint chaining and numerical reasoning.
- Exact match scoring is strict; partial credit or approximate answers are not accepted, which may overstate clinical utility gaps.

## Evidence (verbatim from paper)

> Table 2 presents the projected Success Rate (SR; exact match) across three reasoning categories — data retrieval, aggregation, and threshold/conditional logic, each evaluated on an extended set of 200 synthetic tasks designed to target known failure scenarios.

## Citation

```bibtex
@misc{mantravadi2026art,
  title={ART: Action-based Reasoning Task Benchmarking for Medical AI Agents},
  author={Mantravadi et al. (2026)},
  year={2026},
  note={arXiv:2601.08988}
}
```

- arXiv: 2601.08988

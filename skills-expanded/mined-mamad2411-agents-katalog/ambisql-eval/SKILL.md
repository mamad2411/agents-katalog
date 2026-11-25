---
name: ambisql-eval
description: Evaluates a Text-to-SQL system's ability to generate correct SQL from ambiguous natural language queries when integrated with an interactive ambiguity resolution module. It also measures the system's precision, recall, and F1 in detecting and classifying specific types of schema-mapping and reasoning ambiguities. Use when the user wants to benchmark on AmbiSQL Constructed Dataset, or asks about evaluating this task. Reports Exact Match accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.15276
  bibtex_key: ding2025ambisql
  confidence: high
---

# ambisql-eval

> AmbiSQL: Interactive Ambiguity Detection and Resolution for Text-to-SQL — Ding et al. (2025) (arXiv:2508.15276, 2025)

## What this evaluates

Evaluates a Text-to-SQL system's ability to generate correct SQL from ambiguous natural language queries when integrated with an interactive ambiguity resolution module. It also measures the system's precision, recall, and F1 in detecting and classifying specific types of schema-mapping and reasoning ambiguities.

## Datasets

- **AmbiSQL Constructed Dataset** — total 40; splits: test (40); repo https://github.com/JustinzjDing/AmbiSQL

## Metrics

- `Exact Match accuracy` **(primary)** — range: percent
  - 1 if the generated SQL string exactly matches the ground-truth SQL string, 0 otherwise. Averaged over the dataset.
- `Precision` — range: percent
  - Proportion of detected ambiguous phrases that are correctly identified according to the ambiguity taxonomy.
- `Recall` — range: percent
  - Proportion of actual ambiguous phrases correctly identified by the system.
- `F1-Score` — range: percent
  - Harmonic mean of Precision and Recall for ambiguity detection and classification.

## Input / output format

**Input**: Natural language query, target database dialect, and specific database name. Evaluated without additional user-specified constraints.

**Output**: Generated SQL statement (for generation task); detected ambiguity categories and multiple-choice clarification options (for detection task).

## Scoring recipe

```python
# SQL Generation
exact_match = 1.0 if generated_sql == ground_truth_sql else 0.0
accuracy = sum(exact_match) / len(dataset)

# Ambiguity Detection
tp = sum(1 for pred, gold in zip(predictions, golds) if pred == gold)
fp = sum(1 for pred, gold in zip(predictions, golds) if pred != gold and pred is not None)
fn = sum(1 for pred, gold in zip(predictions, golds) if pred is None and gold is not None)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
```

## Common pitfalls

- Evaluation relies on a small constructed dataset of only 40 queries rather than a large standard benchmark split.
- LLM-related ambiguities show lower recall due to reliance on inconsistent external knowledge, while DB-related ambiguities show higher recall but lower precision due to over-detection.
- Exact match is used for SQL correctness, which is strict and may penalize semantically equivalent but syntactically different queries.

## Evidence (verbatim from paper)

> We evaluated AmbiSQL on two key aspects: (1) end-to-end SQL generation improvements when integrated with existing Text-to-SQL systems, and (2) accuracy of ambiguity detection and classification. For SQL generation, we report accuracy improvements achieved by AmbiSQL on our constructed dataset using Exact Match accuracy to measure correctness. For ambiguity detection, we evaluate AmbiSQL’s precision, recall, and F1-score in identifying and classifying ambiguous phrases according to our taxonomy.

## Citation

```bibtex
@misc{ding2025ambisql,
  title={AmbiSQL: Interactive Ambiguity Detection and Resolution for Text-to-SQL},
  author={Ding et al. (2025)},
  year={2025},
  note={arXiv:2508.15276}
}
```

- arXiv: 2508.15276

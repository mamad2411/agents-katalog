---
name: araspider-eval
description: Evaluates the quality of English-to-Arabic translations for text-to-SQL tasks and measures the execution accuracy of generated SQL queries on Arabic natural language questions. Use when the user wants to benchmark on AraSpider, or asks about evaluating this task. Reports Execution accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.07448
  bibtex_key: heakl2024araspider
  confidence: high
---

# araspider-eval

> AraSpider: Democratizing Arabic-to-SQL — Heakl et al. (2024) (arXiv:2402.07448, 2024)

## What this evaluates

Evaluates the quality of English-to-Arabic translations for text-to-SQL tasks and measures the execution accuracy of generated SQL queries on Arabic natural language questions.

## Datasets

- **AraSpider** — total ?; splits: test (-1)

## Metrics

- `Translation Score` — range: other
  - Average score across all sentences multiplied by 100: (Sum of sentence scores / total number of sentences) × 100. Scores are assigned by ChatGPT-3.5 on a 0–10 scale per sentence.
- `Execution accuracy` **(primary)** — range: percent
  - Binary indicator (1 if the output of the predicted SQL query on the database matches the output of the gold SQL query, 0 otherwise), averaged over all test instances. Accounts for multiple valid SQL queries.

## Input / output format

**Input**: Arabic natural language question (optionally preceded by database schema context). For back-translation evaluation, the input is first translated to English via ChatGPT-3.5 before being fed to the SQL generator.

**Output**: A SQL query string corresponding to the input question.

## Scoring recipe

```python
def compute_execution_accuracy(predictions, golds, databases):
    correct = 0
    for pred_sql, gold_sql, db in zip(predictions, golds, databases):
        pred_out = execute_sql(pred_sql, db)
        gold_out = execute_sql(gold_sql, db)
        if pred_out == gold_out:
            correct += 1
    return (correct / len(predictions)) * 100
```

## Common pitfalls

- Execution accuracy depends heavily on the database schema and context provided; missing schema details cause false negatives.
- Back-translation to English introduces linguistic noise that can degrade SQL generation quality compared to direct English inputs.
- Translation evaluation uses ChatGPT-3.5 as an automated judge, which may exhibit bias or inconsistency compared to human raters.

## Evidence (verbatim from paper)

> Execution accuracy is determined by comparing the predicted query's output with the gold standard query, with consideration given to multiple correct queries as advantageous.

## Citation

```bibtex
@misc{heakl2024araspider,
  title={AraSpider: Democratizing Arabic-to-SQL},
  author={Heakl et al. (2024)},
  year={2024},
  note={arXiv:2402.07448}
}
```

- arXiv: 2402.07448

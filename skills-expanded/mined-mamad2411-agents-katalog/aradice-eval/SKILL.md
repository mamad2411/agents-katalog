---
name: aradice-eval
description: Evaluates LLMs' capabilities in understanding and generating dialectal Arabic (Levantine, Egyptian, Gulf) and assessing cultural awareness. It probes dialect identification, text generation, cognitive reasoning, and machine translation across dialects diverging from Modern Standard Arabic. Use when the user wants to benchmark on AraDiCE, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.11404
  bibtex_key: mousi2024aradice
  confidence: medium
---

# aradice-eval

> AraDiCE: Benchmarks for Dialectal and Cultural Capabilities in LLMs — Basel Mousi et al. (2024) (arXiv:2409.11404, 2024)

## What this evaluates

Evaluates LLMs' capabilities in understanding and generating dialectal Arabic (Levantine, Egyptian, Gulf) and assessing cultural awareness. It probes dialect identification, text generation, cognitive reasoning, and machine translation across dialects diverging from Modern Standard Arabic.

## Datasets

- **AraDiCE** — total ?; splits: test (-1)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Macro-averaged F1 score computed across dialect classes for the dialect identification task.
- `normalized accuracy` — range: [0, 1]
  - Accuracy score normalized to account for class imbalance or task-specific scaling in cognitive reasoning tasks.
- `SacreBLEU` — range: [0, 100]
  - Standardized BLEU score with sentence-level tokenization and Chinese-style punctuation handling, used for machine translation evaluation.

## Input / output format

**Input**: Zero-shot prompts provided in English, Modern Standard Arabic (MSA), or specific dialects depending on the task, formatted for the LM Evaluation Harness.

**Output**: Model-generated text responses or multiple-choice selections, depending on whether the task is generation, identification, or cognitive reasoning.

## Scoring recipe

```python
def compute_metrics(predictions, golds, task_type):
    if task_type == 'dialect_id':
        return f1_score(golds, predictions, average='macro')
    elif task_type == 'cognitive':
        return accuracy_score(golds, predictions)
    elif task_type == 'mt':
        return sacrebleu.corpus_bleu(predictions, [golds]).score
```

## Common pitfalls

- Experiments strictly use zero-shot prompting; few-shot settings are explicitly excluded to reduce computational cost.
- Datasets are synthetically generated via machine translation from English to MSA and then to dialects, followed by human post-editing, which may introduce translation artifacts.
- Evaluation relies on the LM Evaluation Harness, so custom prompt formatting or harness-specific configurations must be matched exactly to reproduce results.

## Evidence (verbatim from paper)

> We used the LM Evaluation Harness for both generation and multiple-choice tasks, employing standard metrics for each task and dataset. We used F1 scores for dialect identification, normalized accuracy for cognitive tasks, and SacreBLEU for machine translation.

## Citation

```bibtex
@misc{mousi2024aradice,
  title={AraDiCE: Benchmarks for Dialectal and Cultural Capabilities in LLMs},
  author={Basel Mousi et al. (2024)},
  year={2024},
  note={arXiv:2409.11404}
}
```

- arXiv: 2409.11404

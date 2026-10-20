---
name: agieval-eval
description: This benchmark evaluates foundation models on human-level cognitive abilities and general reasoning by testing them on a diverse collection of standardized admission and qualification exams. It probes domain-specific knowledge, analytical reasoning, and problem-solving across subjects like mathematics, law, logic, and languages. Use when the user wants to benchmark on AGIEval, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2304.06364
  bibtex_key: zhong2023agieval
  confidence: high
---

# agieval-eval

> AGIEval: A Human-Centric Benchmark for Evaluating Foundation Models — Zhong et al. (2023) (arXiv:2304.06364, 2023)

## What this evaluates

This benchmark evaluates foundation models on human-level cognitive abilities and general reasoning by testing them on a diverse collection of standardized admission and qualification exams. It probes domain-specific knowledge, analytical reasoning, and problem-solving across subjects like mathematics, law, logic, and languages.

## Datasets

- **AGIEval** — total 8062; splits: test (8062); repo https://github.com/ruixiangcui/AGIEval

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard classification accuracy: the proportion of multiple-choice questions where the model's predicted option exactly matches the ground-truth answer.
- `exact-match` — range: [0, 1]
  - Exact Match (EM): the proportion of fill-in-the-blank questions where the model's generated string exactly matches the ground-truth answer string.
- `F1` — range: [0, 1]
  - F1 score: the harmonic mean of token-level precision and recall computed for fill-in-the-blank questions.

## Input / output format

**Input**: A single question from a standardized exam (multiple-choice or fill-in-the-blank), provided in either English or Chinese, often accompanied by context or problem statements.

**Output**: For multiple-choice: the selected option letter or text. For fill-in-the-blank: the exact string or number to complete the sentence/question.

## Scoring recipe

```python
def score_agieval(predictions, golds, formats):
    acc_correct = 0
    em_correct = 0
    for pred, gold, fmt in zip(predictions, golds, formats):
        if fmt == 'multiple_choice':
            if pred.strip().upper() == gold.strip().upper():
                acc_correct += 1
        elif fmt == 'fill_in_blank':
            if pred.strip() == gold.strip():
                em_correct += 1
    total = len(predictions)
    return {
        'accuracy': acc_correct / total,
        'exact_match': em_correct / total
    }
```

## Common pitfalls

- The benchmark explicitly excludes subjective/open-ended questions, so it only evaluates objective formats (MC and fill-in-the-blank).
- Human performance baselines are not obtained by direct testing on the exact subset; they are estimated by scaling the average (50%) and top (1%) test-taker scores from the original exams to 100%.
- The dataset is bilingual (English and Chinese), and models must handle both languages without explicit language-specific tuning.

## Evidence (verbatim from paper)

> The benchmark questions consist of objective formats: multiple-choice and fill-in-the-blank questions. For multiple-choice questions, we adopt standard classification accuracy as the evaluation metric. For fill-in-the-blank questions, we employ Exact Match (EM) and F1 metrics.

## Citation

```bibtex
@misc{zhong2023agieval,
  title={AGIEval: A Human-Centric Benchmark for Evaluating Foundation Models},
  author={Zhong et al. (2023)},
  year={2023},
  note={arXiv:2304.06364}
}
```

- arXiv: 2304.06364

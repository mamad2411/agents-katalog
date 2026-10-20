---
name: autodrive-qa-eval
description: Evaluates vision-language models on urban autonomous driving tasks by testing their ability to answer multiple-choice questions covering perception, prediction, and planning. It probes domain-specific reasoning, hazard detection, speed judgment, and object classification in driving scenarios. Use when the user wants to benchmark on AutoDrive-QA, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.15778
  bibtex_key: khalili2025autodriveqa
  confidence: high
---

# autodrive-qa-eval

> AutoDrive-QA: A Multiple-Choice Benchmark for Vision-Language Evaluation in Urban Autonomous Driving — Khalili and Smyth (2025) (arXiv:2503.15778, 2025)

## What this evaluates

Evaluates vision-language models on urban autonomous driving tasks by testing their ability to answer multiple-choice questions covering perception, prediction, and planning. It probes domain-specific reasoning, hazard detection, speed judgment, and object classification in driving scenarios.

## Datasets

- **AutoDrive-QA** — total 15400; splits: full (15400); repo https://github.com/Boshrakh/AutoDrive-QA

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly answered multiple-choice questions out of the total number of questions.

## Input / output format

**Input**: An image frame from an autonomous driving scenario, accompanied by a multiple-choice question with one correct answer and three distractors.

**Output**: A single selected option (A, B, C, or D) corresponding to the correct answer.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for pred, gold in zip(predictions, gold_labels) if pred == gold)
    return correct / len(gold_labels)
```

## Common pitfalls

- Distractors are generated from five specific error categories (e.g., Driving Domain Misconceptions, Logical Inconsistencies), so models may fail on specific reasoning types rather than general vision-language understanding.
- Option order is randomized to avoid positional bias, so models must rely on content rather than answer position.

## Evidence (verbatim from paper)

> To validate clarity and answerability, human experts solved 400 randomly sampled questions. They achieved nearly 100% accuracy on perception and over 97.5% accuracy on prediction and planning, confirming that the questions are unambiguous for domain experts while still challenging for VLMs.

## Citation

```bibtex
@misc{khalili2025autodriveqa,
  title={AutoDrive-QA: A Multiple-Choice Benchmark for Vision-Language Evaluation in Urban Autonomous Driving},
  author={Khalili and Smyth (2025)},
  year={2025},
  note={arXiv:2503.15778}
}
```

- arXiv: 2503.15778

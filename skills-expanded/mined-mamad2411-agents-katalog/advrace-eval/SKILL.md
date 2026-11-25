---
name: advrace-eval
description: Evaluates the robustness of machine reading comprehension models against four adversarial perturbations (AddSent, CharSwap, Distractor Extraction, and Distractor Generation) applied to passages, questions, and answer options. It measures how much model accuracy degrades when faced with label-preserving but semantically altered inputs compared to clean data. Use when the user wants to benchmark on AdvRACE, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.14004
  bibtex_key: si2020benchmarking
  confidence: high
---

# advrace-eval

> Benchmarking Robustness of Machine Reading Comprehension Models — Chenglei Si et al. (arXiv:2004.14004, 2020)

## What this evaluates

Evaluates the robustness of machine reading comprehension models against four adversarial perturbations (AddSent, CharSwap, Distractor Extraction, and Distractor Generation) applied to passages, questions, and answer options. It measures how much model accuracy degrades when faced with label-preserving but semantically altered inputs compared to clean data.

## Datasets

- **AdvRACE** — total 4934; splits: test (4934); repo https://github.com/NoviScl/AdvRACE

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Exact-match accuracy calculated as the number of correctly predicted answer choices divided by the total number of examples in the adversarial test set.
- `percentage performance drop` — range: percent
  - Relative degradation in accuracy compared to the original clean test set, calculated as (1 - accuracy_adv / accuracy_orig) * 100.

## Input / output format

**Input**: A reading comprehension instance consisting of a passage, a question, and four candidate answer options. Models concatenate each candidate answer with the passage and question to form four separate input sequences for encoding.

**Output**: A single predicted answer choice (A, B, C, or D) for each question, derived from the [CLS] token representation passed through a fully-connected layer.

## Scoring recipe

```python
def compute_metrics(predictions, gold_labels, clean_accuracy):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    adv_accuracy = correct / len(gold_labels)
    performance_drop = (1 - adv_accuracy / clean_accuracy) * 100
    return {'accuracy': adv_accuracy, 'percentage_performance_drop': performance_drop}
```

## Common pitfalls

- Confusing the AdvRACE adversarial subsets with the original RACE test set; each adversarial subset contains exactly 4,934 examples, not the full RACE corpus.
- Calculating performance drop as an absolute difference instead of the relative percentage drop relative to the original test set accuracy as specified in the paper.
- Assuming adversarial examples are unanswerable; the benchmark strictly preserves the original correct answers, and the 'unanswerable' option was only introduced for human validation, not model evaluation.

## Evidence (verbatim from paper)

> In addition to reporting the accuracy of each model on each test set, we also report the percentage performance drop relative to the performance on the original test set for the adversarial test sets.

## Citation

```bibtex
@misc{si2020benchmarking,
  title={Benchmarking Robustness of Machine Reading Comprehension Models},
  author={Chenglei Si et al.},
  year={2020},
  note={arXiv:2004.14004}
}
```

- arXiv: 2004.14004

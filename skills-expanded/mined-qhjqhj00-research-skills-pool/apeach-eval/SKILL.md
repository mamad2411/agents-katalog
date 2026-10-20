---
name: apeach-eval
description: Evaluates the ability of NLP models to detect hate speech in Korean text. It specifically probes domain-agnostic generalizability and resistance to common inductive biases like text length or topic distribution. Use when the user wants to benchmark on APEACH, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2202.12459
  bibtex_key: yang2022apeach
  confidence: medium
---

# apeach-eval

> APEACH: Attacking Pejorative Expressions with Analysis on Crowd-Generated Hate Speech Evaluation Datasets — Yang et al. (2022) (arXiv:2202.12459, 2022)

## What this evaluates

Evaluates the ability of NLP models to detect hate speech in Korean text. It specifically probes domain-agnostic generalizability and resistance to common inductive biases like text length or topic distribution.

## Datasets

- **APEACH** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard binary classification accuracy: the proportion of correctly classified instances (hate speech vs. non-hate speech) out of the total evaluation set.

## Input / output format

**Input**: Korean text sentences, optionally accompanied by a topic category from a predefined list of 10 discrimination/hate speech themes.

**Output**: Binary label: 'hate speech' (positive) or 'non-hate speech' (negative).

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Models may exploit text length bias, as hate speech instances are often longer than neutral ones.
- Topic prompt ordering can cause workers to default to top dropdown options, creating distributional skew.
- Pretraining data overlap can artificially inflate performance on domain-specific hate speech benchmarks.

## Evidence (verbatim from paper)

> In our study, the hate speech (positive sample) and non-hate speech (negative sample) serve as an element of the balanced dataset for the detection task.

## Citation

```bibtex
@misc{yang2022apeach,
  title={APEACH: Attacking Pejorative Expressions with Analysis on Crowd-Generated Hate Speech Evaluation Datasets},
  author={Yang et al. (2022)},
  year={2022},
  note={arXiv:2202.12459}
}
```

- arXiv: 2202.12459

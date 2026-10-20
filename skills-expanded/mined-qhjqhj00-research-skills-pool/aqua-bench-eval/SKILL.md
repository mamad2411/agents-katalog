---
name: aqua-bench-eval
description: This benchmark evaluates audio question answering models on their ability to correctly answer standard multiple-choice questions and, crucially, to detect and reject unanswerable cases. It specifically probes three failure modes: missing correct options, categorical mismatches between questions and answers, and questions irrelevant to the audio input. Use when the user wants to benchmark on AQUA-Bench, or asks about evaluating this task. Reports conditional accuracy (CA).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.12248
  bibtex_key: kuan2026aquabench
  confidence: high
---

# aqua-bench-eval

> AQUA-Bench: Beyond Finding Answers to Knowing When There Are None in Audio Question Answering — Kuan et al. (2026) (arXiv:2601.12248, 2026)

## What this evaluates

This benchmark evaluates audio question answering models on their ability to correctly answer standard multiple-choice questions and, crucially, to detect and reject unanswerable cases. It specifically probes three failure modes: missing correct options, categorical mismatches between questions and answers, and questions irrelevant to the audio input.

## Datasets

- **AQUA-Bench** — total ?; splits: test (-1); repo https://kuan2jiu99.github.io/AQUA-Bench-demo/

## Metrics

- `accuracy` — range: [0, 1]
  - Standard multiple-choice accuracy: fraction of correctly predicted options from the candidate set on the original answerable subset.
- `conditional accuracy (CA)` **(primary)** — range: [0, 1]
  - Conditional accuracy: a prediction on an unanswerable case is only counted if the model correctly answered the corresponding solvable counterpart. Measures the ability to recognize unanswerability independent of base task errors.

## Input / output format

**Input**: An audio clip A, a natural language question Q, and a candidate answer set C formatted as multiple-choice options (a)–(e).

**Output**: The model must output the correct option letter/text if the question is answerable, or a designated rejection response (e.g., "None of the above" or "Unanswerable") if the question is unanswerable.

## Scoring recipe

```python
def compute_conditional_accuracy(preds, golds, base_correct):
    # base_correct: boolean array indicating if model got the solvable counterpart right
    valid_mask = base_correct
    correct_reject = (preds == golds) & valid_mask
    ca = correct_reject.sum() / valid_mask.sum()
    return ca
```

## Common pitfalls

- Conditional accuracy (CA) inherently penalizes models that fail the base audio comprehension task, even if they correctly identify unanswerable questions, making it difficult to isolate rejection capability from general understanding.
- The fixed multiple-choice template with a mandatory "None of the above" option may encourage models to guess the rejection label without genuine audio reasoning or semantic alignment.
- IAQD instances for the MMAU subset are generated via GPT-4o, which may introduce subtle phrasing biases or unnatural question structures compared to human-written benchmarks.

## Evidence (verbatim from paper)

> We adopt a two-stage evaluation protocol. First, models are tested on the original answerable subset of each benchmark, where accuracy is reported to measure core audio understanding. Next, we evaluate the three unanswerable subsets, AAD, IASD, and IAQD, using conditional accuracy (CA). Specifically, a model’s prediction on an unanswerable case is only counted if it correctly answered the corresponding solvable counterpart. This ensures that performance reflects the ability to recognize unanswerability, rather than being confounded by errors on the original task.

## Citation

```bibtex
@misc{kuan2026aquabench,
  title={AQUA-Bench: Beyond Finding Answers to Knowing When There Are None in Audio Question Answering},
  author={Kuan et al. (2026)},
  year={2026},
  note={arXiv:2601.12248}
}
```

- arXiv: 2601.12248

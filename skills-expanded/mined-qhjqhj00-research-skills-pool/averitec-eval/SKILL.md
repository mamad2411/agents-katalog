---
name: averitec-eval
description: Evaluates a model's ability to verify real-world claims by retrieving web evidence, generating supporting questions, predicting veracity stance, and producing textual justifications. It probes retrieval quality, stance detection, and justification generation under realistic conditions with temporal and context constraints. Use when the user wants to benchmark on AVeriTeC, or asks about evaluating this task. Reports Macro-F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2305.13117
  bibtex_key: schlichtkrull2023averitec
  confidence: high
---

# averitec-eval

> AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web — Schlichtkrull et al. (2023) (arXiv:2305.13117, 2023)

## What this evaluates

Evaluates a model's ability to verify real-world claims by retrieving web evidence, generating supporting questions, predicting veracity stance, and producing textual justifications. It probes retrieval quality, stance detection, and justification generation under realistic conditions with temporal and context constraints.

## Datasets

- **AVeriTeC** — total ?; splits: train (-1), dev (-1); repo https://github.com/MichSchli/AVeriTeC

## Metrics

- `Macro-F1` **(primary)** — range: [0, 1]
  - Average of per-class F1 scores across four veracity labels: Supported, Refuted, Conflicting evidence/cherrypicking, and Not enough evidence.
- `METEOR` — range: [0, 1]
  - Standard METEOR metric comparing generated justification text against gold justification references, accounting for synonymy and stemming.
- `AVERITEC score` — range: [0, 1]
  - A thresholded evaluation metric for veracity and justification, computed at a similarity threshold lambda (recommended 0.25). Scores reflect how well predicted evidence and verdicts align with gold annotations under this cutoff.

## Input / output format

**Input**: Claim text, optionally accompanied by retrieved web documents/sentences and generated questions.

**Output**: Veracity label (Supported, Refuted, Conflicting evidence/cherrypicking, or Not enough evidence), generated questions, retrieved evidence sentences, and a textual justification.

## Scoring recipe

```python
def compute_macro_f1(predictions, gold):
    classes = ['Supported', 'Refuted', 'Conflicting evidence/cherrypicking', 'Not enough evidence']
    f1_scores = []
    for cls in classes:
        tp = sum(1 for p, g in zip(predictions, gold) if p == cls and g == cls)
        fp = sum(1 for p, g in zip(predictions, gold) if p == cls and g != cls)
        fn = sum(1 for p, g in zip(predictions, gold) if p != cls and g == cls)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1_scores.append(f1)
    return sum(f1_scores) / len(f1_scores)

# METEOR is computed via standard library against gold justifications
# AVERITEC score applies threshold lambda (e.g., 0.25) to veracity/justification alignment
```

## Common pitfalls

- Retrieval systems often rely on wrong evidence rather than paraphrasing, which standard metrics may penalize unfairly.
- Stance detection models frequently produce false positives for 'Conflicting evidence/cherrypicking' when context-adding questions are misclassified as refuting.
- Threshold selection (lambda) significantly impacts scores; lambda=0.25 is recommended over stricter cutoffs.
- LLMs like ChatGPT may achieve high veracity accuracy but fail to provide valid evidence, leading to hallucinated justifications.

## Evidence (verbatim from paper)

> We tested three different models for veracity prediction: BERT-large, bloom-7b1, and Vicuna-13b. We found BERT to perform better by a slight margin; using gold evidence, we obtained macro-F1 scores of .49, .43, and .48 for the three models respectively.

## Citation

```bibtex
@misc{schlichtkrull2023averitec,
  title={AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web},
  author={Schlichtkrull et al. (2023)},
  year={2023},
  note={arXiv:2305.13117}
}
```

- arXiv: 2305.13117

---
name: acronym-id-disamb-eval
description: Evaluates a model's ability to identify acronym boundaries and their corresponding long forms in scientific text, and to disambiguate ambiguous acronyms by selecting the correct long form from a candidate set. Use when the user wants to benchmark on SciAI, SciAD, or asks about evaluating this task. Reports Macro F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2010.14678
  bibtex_key: pouranbenveyseh2020acronym
  confidence: high
---

# acronym-id-disamb-eval

> What Does This Acronym Mean? Introducing a New Dataset for Acronym Identification and Disambiguation — Amir Pouran Ben Veyseh et al. (arXiv:2010.14678, 2020)

## What this evaluates

Evaluates a model's ability to identify acronym boundaries and their corresponding long forms in scientific text, and to disambiguate ambiguous acronyms by selecting the correct long form from a candidate set.

## Datasets

- **SciAI** — total 17506; splits: train (-1), val (-1), test (-1)
- **SciAD** — total 62441; splits: train (-1), val (-1), test (-1)

## Metrics

- `Macro F1` **(primary)** — range: percent
  - Harmonic mean of macro-averaged precision and recall. Computed by averaging F1 scores across all individual acronyms or long forms, giving equal weight to each class regardless of frequency.
- `Precision` — range: percent
  - Ratio of correct predictions to total predicted instances, macro-averaged across all classes.
- `Recall` — range: percent
  - Ratio of correct predictions to total actual instances, macro-averaged across all classes.

## Input / output format

**Input**: Sentence containing an acronym (for AI) or an acronym with surrounding context and candidate long forms (for AD).

**Output**: For AI: predicted character boundaries for the acronym and its long form. For AD: predicted long form string from the candidate set.

## Scoring recipe

```python
def compute_macro_f1(predictions, golds):
    f1_scores = []
    for pred, gold in zip(predictions, golds):
        correct = (pred == gold)
        tp = 1 if correct else 0
        fp = 1 if not correct else 0
        fn = 1 if not correct else 0
        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        f1_scores.append(f1)
    return sum(f1_scores) / len(f1_scores)
```

## Common pitfalls

- Strict boundary matching required for AI: predictions must exactly match ground-truth character spans.
- Macro-averaging is used, which weights each acronym/long form equally rather than weighting by frequency, making it sensitive to rare acronyms.
- Domain shift is significant: models evaluated on general domain datasets (UAD) will show inflated performance compared to scientific domain (SciAD).

## Evidence (verbatim from paper)

> For AI, a prediction of acronym or long form is counted as true if the boundaries of the prediction matches with the boundary of the ground-truth acronym or long form in the sentence, respectively. We report the macro-averaged precision, recall and F1 score computed for acronym and long form prediction. For AD, similar to prior work (Ciosici et al., 2019), we report the performance of the models using macro-averaged precision, recall and F1 score computed for each long form.

## Citation

```bibtex
@misc{pouranbenveyseh2020acronym,
  title={What Does This Acronym Mean? Introducing a New Dataset for Acronym Identification and Disambiguation},
  author={Amir Pouran Ben Veyseh et al.},
  year={2020},
  note={arXiv:2010.14678}
}
```

- arXiv: 2010.14678

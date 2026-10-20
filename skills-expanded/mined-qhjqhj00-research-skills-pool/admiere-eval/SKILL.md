---
name: admiere-eval
description: Evaluates a model's ability to understand and represent multimodal idiomaticity by ranking images based on their alignment with a given context sentence containing a nominal compound. It probes vision-language model alignment, figurative language reasoning, and the capacity to distinguish between literal and idiomatic senses. Use when the user wants to benchmark on AdMIRe, or asks about evaluating this task. Reports Top Image Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.15358
  bibtex_key: pickard2025admiere
  confidence: high
---

# admiere-eval

> SemEval-2025 Task 1: AdMIRe -- Advancing Multimodal Idiomaticity Representation — Pickard et al. (2025) (arXiv:2503.15358, 2025)

## What this evaluates

Evaluates a model's ability to understand and represent multimodal idiomaticity by ranking images based on their alignment with a given context sentence containing a nominal compound. It probes vision-language model alignment, figurative language reasoning, and the capacity to distinguish between literal and idiomatic senses.

## Datasets

- **AdMIRe** — total 155; splits: train (102), dev (25), test (28), extended_eval (100)

## Metrics

- `Top Image Accuracy` **(primary)** — range: [0, 1]
  - Measures the fraction of instances where the model correctly identifies the most representative image as rank 1 in the predicted ranking.
- `Discounted Cumulative Gain (DCG)` — range: [0, 3.631]
  - Defined as DCG_n = sum_{i=1}^n (rel_i / log_2(i+1)). The paper uses fixed positional relevance weights of [3, 1, 0, 0, 0] for the five ranked images, yielding a maximum possible score of 3.631. It captures both relevance and correct ordering without penalizing permutations of low-relevance items.

## Input / output format

**Input**: A context sentence containing a nominal compound and a set of five images (or text captions describing them). For Subtask B, the first two images of a narrative sequence and four candidate completion images.

**Output**: A ranked list of the five images (or captions) ordered by relevance to the context sentence's meaning. For Subtask B, the index of the correct completion image and a binary classification of the sense (literal vs. idiomatic).

## Scoring recipe

```python
import math

def score(predictions, gold):
    # predictions: list of 5 image indices ranked by model
    # gold: index of the strongly associated image
    top1_acc = 1.0 if predictions[0] == gold else 0.0
    # DCG with fixed positional weights [3, 1, 0, 0, 0]
    weights = [3, 1, 0, 0, 0]
    dcg = sum(weights[i] / math.log2(i + 2) for i in range(5))
    return top1_acc, dcg
```

## Common pitfalls

- The DCG metric uses fixed positional weights [3, 1, 0, 0, 0] rather than dynamically assigning relevance based on the gold label, meaning permutations of the bottom three images do not affect the score.
- The extended evaluation set intentionally uses the opposite sense of the nominal compounds found in the primary test set, requiring models to generalize across literal/idiomatic shifts rather than just memorizing test items.
- Subtask A supports both multimodal (image) and monomodal (text caption) settings, and models must be evaluated separately for each to avoid cross-modal leakage.

## Evidence (verbatim from paper)

> Performance for Subtask A is assessed with two key metrics: a) Top Image Accuracy, which measures only the correct identification of the most representative image and b) Discounted Cumulative Gain (DCG) (Järvelin and Kekäläinen, 2002), an established information retrieval metric that not only captures the fraction of retrieved relevant information but also takes into account their correct ordering. ... Because our expected order of images is somewhat arbitrary ... we adopt a weighting of [3,1,0,0,0] for the five image positions; this allows the metric to capture some of the relevant semantics beyond the top image accuracy without penalising systems which permute the order of the low-relevance images.

## Citation

```bibtex
@misc{pickard2025admiere,
  title={SemEval-2025 Task 1: AdMIRe -- Advancing Multimodal Idiomaticity Representation},
  author={Pickard et al. (2025)},
  year={2025},
  note={arXiv:2503.15358}
}
```

- arXiv: 2503.15358

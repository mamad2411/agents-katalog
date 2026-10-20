---
name: aspect-extraction-eval
description: Evaluates a model's ability to identify aspect terms (targets), their categories, sentiment polarity, and exact character positions within restaurant review sentences in Turkish. Use when the user wants to benchmark on SemEval 2016 Turkish Restaurant Reviews, SemEval 2016 English-Translated Restaurant Reviews, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.03512
  bibtex_key: erkan2025aspect
  confidence: high
---

# aspect-extraction-eval

> An Aspect Extraction Framework using Different Embedding Types, Learning Models, and Dependency Structure — Erkan et al. (2025) (arXiv:2503.03512, 2025)

## What this evaluates

Evaluates a model's ability to identify aspect terms (targets), their categories, sentiment polarity, and exact character positions within restaurant review sentences in Turkish.

## Datasets

- **SemEval 2016 Turkish Restaurant Reviews** — total 1248; splits: train (1104), test (144); repo https://github.com/alierkan/Turkish-ABSA
- **SemEval 2016 English-Translated Restaurant Reviews** — total 2676; splits: train (2000), test (676); repo https://github.com/alierkan/Turkish-ABSA

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall for correctly predicted aspect spans and attributes. Calculated per aspect instance across the test set.

## Input / output format

**Input**: Raw text of a sentence or review.

**Output**: Structured prediction containing aspect target string, category, polarity, and character span indices (from-to).

## Scoring recipe

```python
def compute_f1(predictions, gold):
    correct = 0
    for pred, gold_item in zip(predictions, gold):
        if (pred['target'] == gold_item['target'] and
            pred['category'] == gold_item['category'] and
            pred['polarity'] == gold_item['polarity'] and
            pred['from'] == gold_item['from'] and
            pred['to'] == gold_item['to']):
            correct += 1
    precision = correct / len(predictions) if predictions else 0
    recall = correct / len(gold) if gold else 0
    return 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
```

## Common pitfalls

- Translation-induced position shifts require careful relabeling of aspect spans.
- Aspect term normalization is critical to avoid counting identical concepts as different spans.
- XML format requires parsing nested sentence and opinion tags correctly.

## Evidence (verbatim from paper)

> The SemEval Restaurant Reviews datasets are stored in XML format. Listing [1] shows an example review from the English Restaurant Reviews dataset. A review is formed of a number of sentences. Each sentence includes zero or more aspect/sentiment information which is composed of an aspect ("target"), category of the aspect ("category"), sentiment for the aspect ("polarity"), and the position of the aspect within the sentence ("from"-"to").

## Citation

```bibtex
@misc{erkan2025aspect,
  title={An Aspect Extraction Framework using Different Embedding Types, Learning Models, and Dependency Structure},
  author={Erkan et al. (2025)},
  year={2025},
  note={arXiv:2503.03512}
}
```

- arXiv: 2503.03512

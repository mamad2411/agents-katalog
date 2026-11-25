---
name: ace2005-ner-eval
description: Evaluates the ability of pretrained models to recognize named entities in open-domain text, specifically probing generalization when name regularity and mention coverage are manipulated. It measures how well models rely on contextual patterns versus superficial spelling cues. Use when the user wants to benchmark on ACE2005, or asks about evaluating this task. Reports Micro-F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2004.12126
  bibtex_key: lin2020rigorous
  confidence: high
---

# ace2005-ner-eval

> A Rigorous Study on Named Entity Recognition: Can Fine-tuning Pretrained Model Lead to the Promised Land? — Lin et al. (2020) (arXiv:2004.12126, 2020)

## What this evaluates

Evaluates the ability of pretrained models to recognize named entities in open-domain text, specifically probing generalization when name regularity and mention coverage are manipulated. It measures how well models rely on contextual patterns versus superficial spelling cues.

## Datasets

- **ACE2005** — total ?; splits: train (18739), dev (2531), test (2314)

## Metrics

- `Micro-F1` **(primary)** — range: [0, 1]
  - Standard micro-averaged F1 score computed globally across all entity mentions and classes. Precision and Recall are aggregated across the entire dataset before computing F1 = 2 * (Precision * Recall) / (Precision + Recall).

## Input / output format

**Input**: Raw text sequences containing named, nominal, and pronominal mentions.

**Output**: Sequence of entity type labels (PER, ORG, GPE, FAC, LOC, WEA, VEH) for each token/mention, typically using a BIO-style tagging scheme.

## Scoring recipe

```python
def compute_micro_f1(predictions, golds):
    tp = fp = fn = 0
    for p, g in zip(predictions, golds):
        if p == g:
            tp += 1
        else:
            if p != 'O': fp += 1
            if g != 'O': fn += 1
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
```

## Common pitfalls

- 58.4% of test mentions appear in the training data, causing models to overfit to observed entities rather than generalizing to unseen ones.
- Standard benchmarks mask the heavy reliance on name regularity (spelling patterns), making models appear more context-aware than they actually are.

## Evidence (verbatim from paper)

> For all experiments, we only consider the outmost mentions similar to the majority of the previous work. Finally, there are 18739/2531/2314 mentions in the train/dev/test set respectively. We found that 58.4% mentions in the test set have appeared in the training data, which confirms our high mention coverage concern. ... Table 2: Micro-F1 scores of BERT-CRF tagger on original data, name permutation setting and mention permutation setting respectively.

## Citation

```bibtex
@misc{lin2020rigorous,
  title={A Rigorous Study on Named Entity Recognition: Can Fine-tuning Pretrained Model Lead to the Promised Land?},
  author={Lin et al. (2020)},
  year={2020},
  note={arXiv:2004.12126}
}
```

- arXiv: 2004.12126

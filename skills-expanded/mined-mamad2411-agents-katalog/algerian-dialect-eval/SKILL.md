---
name: algerian-dialect-eval
description: Evaluates cross-lingual and cross-script transfer performance for sentiment analysis and topic classification on a novel multi-layer Algerian dialect corpus. Probes how script differences (Latin/NArabizi vs. Arabic/Persian/Urdu) and typological similarity impact classification accuracy in code-switched, under-resourced vernaculars. Use when the user wants to benchmark on Algerian Dialect Corpus (NArabizi), or asks about evaluating this task. Reports Macro F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2105.07400
  bibtex_key: touileb2021corpus
  confidence: high
---

# algerian-dialect-eval

> The interplay between language similarity and script on a novel multi-layer Algerian dialect corpus — Touileb et al. (2021) (arXiv:2105.07400, 2021)

## What this evaluates

Evaluates cross-lingual and cross-script transfer performance for sentiment analysis and topic classification on a novel multi-layer Algerian dialect corpus. Probes how script differences (Latin/NArabizi vs. Arabic/Persian/Urdu) and typological similarity impact classification accuracy in code-switched, under-resourced vernaculars.

## Datasets

- **Algerian Dialect Corpus (NArabizi)** — total ?; splits: train (-1), dev (-1), test (-1); repo https://github.com/SamiaTouileb/Narabizi

## Metrics

- `Macro F1` **(primary)** — range: [0, 1]
  - Unweighted mean of the F1 scores computed independently for each class. Calculated as the average of precision and recall per class, then averaged across all classes to mitigate label skew.

## Input / output format

**Input**: Raw text sentences or documents in various scripts (NArabizi/Latin, Arabic, Persian, Urdu, Hebrew, Maltese, MSA).

**Output**: Discrete class label: for sentiment, 'pos' or 'neg'; for topic classification, one of 5 collapsed categories.

## Scoring recipe

```python
def macro_f1(predictions, gold):
    classes = sorted(set(predictions) | set(gold))
    f1_scores = []
    for c in classes:
        tp = sum(1 for p, g in zip(predictions, gold) if p == c and g == c)
        fp = sum(1 for p, g in zip(predictions, gold) if p == c and g != c)
        fn = sum(1 for p, g in zip(predictions, gold) if p != c and g == c)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
        f1_scores.append(f1)
    return sum(f1_scores) / len(f1_scores)
```

## Common pitfalls

- The paper states testing the best model on the 'dev set' rather than a held-out test set, which may indicate a non-standard split or potential data leakage.
- Label distributions are highly skewed; using accuracy instead of Macro F1 would heavily favor majority classes and misrepresent model performance.
- Topic categories 'Prayer' and 'Religion' are explicitly collapsed into a single class, changing the task from its original formulation to a 5-class problem.

## Evidence (verbatim from paper)

> As the label distribution for both tasks is highly skewed, we use Macro F1 to evaluate. Given the size of the categories "Prayer" and "Religion", we collapse them to a single topic, converting the topic classification task into a 5-class multi-class problem.

## Citation

```bibtex
@misc{touileb2021corpus,
  title={The interplay between language similarity and script on a novel multi-layer Algerian dialect corpus},
  author={Touileb et al. (2021)},
  year={2021},
  note={arXiv:2105.07400}
}
```

- arXiv: 2105.07400

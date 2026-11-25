---
name: active-look-hallucination-eval
description: Evaluates the ability of large vision-language models to mitigate object-existence hallucinations by dynamically allocating visual computation based on uncertainty. It probes fine-grained perception, object counting, spatial reasoning, and color recognition under adaptive visual grounding. Use when the user wants to benchmark on POPE, MME, CHAIR, or asks about evaluating this task. Reports POPE Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.24396
  bibtex_key: jiang2026globalcontext
  confidence: high
---

# active-look-hallucination-eval

> Global Context or Local Detail? Adaptive Visual Grounding for Hallucination Mitigation — Jiang et al. (2026) (arXiv:2604.24396, 2026)

## What this evaluates

Evaluates the ability of large vision-language models to mitigate object-existence hallucinations by dynamically allocating visual computation based on uncertainty. It probes fine-grained perception, object counting, spatial reasoning, and color recognition under adaptive visual grounding.

## Datasets

- **POPE** — total ?; splits: test (-1)
- **MME** — total ?; splits: test (-1)
- **CHAIR** — total ?; splits: test (-1)

## Metrics

- `POPE Accuracy` **(primary)** — range: percent
  - Percentage of correctly answered yes/no questions regarding object existence in the image.
- `POPE Recall` — range: percent
  - Ratio of correctly identified existing objects to all ground-truth objects.
- `MME Total Score` — range: score
  - Aggregated performance score across the Existence, Count, Position, and Color categories.
- `CHAIR scores` — range: percent
  - Hallucination rate calculated as the ratio of objects mentioned in the generated caption but absent in the ground-truth annotations.
- `F1` — range: percent
  - Harmonic mean of Accuracy and Recall.

## Input / output format

**Input**: Image paired with a text prompt (yes/no question for POPE/MME, or open-ended captioning prompt for CHAIR).

**Output**: Text response: 'yes'/'no' for POPE/MME existence questions, or a natural language caption for CHAIR.

## Scoring recipe

```python
def score_pope(preds, golds):
    acc = sum(1 for p, g in zip(preds, golds) if p == g) / len(golds)
    tp = sum(1 for p, g in zip(preds, golds) if p == 'yes' and g == 'yes')
    fn = sum(1 for p, g in zip(preds, golds) if p == 'no' and g == 'yes')
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return acc, recall

def score_chair(captions, gt_annotations):
    scores = []
    for cap, gt in zip(captions, gt_annotations):
        cap_objs = extract_objects(cap)
        hallucinated = [o for o in cap_objs if o not in gt]
        score = len(hallucinated) / len(cap_objs) * 100 if cap_objs else 0
        scores.append(score)
    return sum(scores) / len(scores)
```

## Common pitfalls

- Naive stacking of visual tools causes false-positive accumulation rather than improvement.
- Unstructured aggregation of dual-expert proposals propagates conflicting false positives, lowering accuracy.
- Trade-off between global context preservation and local detail enhancement must be carefully balanced to avoid performance drops.

## Evidence (verbatim from paper)

> CHAIR measures object hallucination in image captioning by comparing objects mentioned in captions against ground-truth object annotations. We report CHAIR scores as the hallucination rate of mentioned objects.

## Citation

```bibtex
@misc{jiang2026globalcontext,
  title={Global Context or Local Detail? Adaptive Visual Grounding for Hallucination Mitigation},
  author={Jiang et al. (2026)},
  year={2026},
  note={arXiv:2604.24396}
}
```

- arXiv: 2604.24396

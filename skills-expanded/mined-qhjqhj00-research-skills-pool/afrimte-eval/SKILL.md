---
name: afrimte-eval
description: Evaluates machine translation quality for under-resourced African languages using human-annotated Direct Assessment (DA) scores and error-span annotations. It probes a model's ability to preserve meaning across 13 diverse language pairs. Use when the user wants to benchmark on FLORES-200, or asks about evaluating this task. Reports Direct Assessment (DA) score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.09828
  bibtex_key: wang2023afrimte
  confidence: high
---

# afrimte-eval

> AfriMTE and AfriCOMET: Enhancing COMET to Embrace Under-resourced African Languages — Wang et al. (2023) (arXiv:2311.09828, 2023)

## What this evaluates

Evaluates machine translation quality for under-resourced African languages using human-annotated Direct Assessment (DA) scores and error-span annotations. It probes a model's ability to preserve meaning across 13 diverse language pairs.

## Datasets

- **FLORES-200** — total ?; splits: dev (-1), devtest (-1); repo https://github.com/facebookresearch/flores/tree/main/flores200

## Metrics

- `Direct Assessment (DA) score` **(primary)** — range: [0, 100]
  - A subjective score from 0 to 100 assigned by human annotators, where 0 means 'Nonsense/No meaning preserved' and 100 means 'Perfect meaning'. Intermediate benchmarks are set at 33 ('Some meaning preserved') and 67 ('Most meaning preserved').
- `Spearman-rank correlation` — range: [-1, 1]
  - Measures the monotonic relationship between predicted metric scores and human DA scores. Used to evaluate how well automated metrics align with human judgments.

## Input / output format

**Input**: Source sentence and machine-translated target sentence.

**Output**: DA score (0-100) and highlighted error spans in the source and target texts.

## Scoring recipe

```python
def compute_gold_da(annotator_scores):
    # annotator_scores: dict of {annotator_id: [raw_scores]}
    valid = {k: v for k, v in annotator_scores.items() if max(v) - min(v) <= 34}
    z_scores = {}
    for k, scores in valid.items():
        mean = sum(scores) / len(scores)
        std = (sum((x - mean)**2 for x in scores) / len(scores))**0.5
        z_scores[k] = [(x - mean) / std for x in scores]
    return [sum(z[k][i] for k in z_scores) / len(z_scores) for i in range(len(z_scores[list(z_scores.keys())[0]]))]
```

## Common pitfalls

- Not all annotators consistently highlight error spans, resulting in low DA scores without corresponding spans.
- Raw DA scores are subjective and evaluator-specific; failing to normalize to z-scores before averaging can introduce significant bias.
- The 34-point inconsistency threshold is strict; ignoring it may include unreliable annotations.

## Evidence (verbatim from paper)

> evaluators were instructed to assign a value between 0 and 100 to indicate the extent to which the original meaning was preserved in the translation. ... To reduce biases among evaluators, we normalized the DA scores at the evaluator level to get the z-scores. The final scores for our benchmark modeling were determined by averaging these z-scores across evaluators for each translation.

## Citation

```bibtex
@misc{wang2023afrimte,
  title={AfriMTE and AfriCOMET: Enhancing COMET to Embrace Under-resourced African Languages},
  author={Wang et al. (2023)},
  year={2023},
  note={arXiv:2311.09828}
}
```

- arXiv: 2311.09828

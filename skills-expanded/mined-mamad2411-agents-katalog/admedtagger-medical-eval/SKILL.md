---
name: admedtagger-medical-eval
description: Evaluates the ability of lightweight BERT-based models to classify Polish medical texts into five clinical categories. The benchmark tests knowledge distillation from a large LLM teacher to smaller classifiers, with ground truth curated by medical experts. Use when the user wants to benchmark on ADMEDTAGGER Physician-Validated Test Sets, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.09722
  bibtex_key: gorski2025admedtagger
  confidence: medium
---

# admedtagger-medical-eval

> ADMEDTAGGER: an annotation framework for distillation of expert knowledge for the Polish medical language — Górski et al. (2025) (arXiv:2601.09722, 2025)

## What this evaluates

Evaluates the ability of lightweight BERT-based models to classify Polish medical texts into five clinical categories. The benchmark tests knowledge distillation from a large LLM teacher to smaller classifiers, with ground truth curated by medical experts.

## Datasets

- **ADMEDTAGGER Physician-Validated Test Sets** — total ?; splits: test (-1)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Standard F1 score calculated per clinical category, likely macro-averaged across the five categories. Combines precision and recall into a single harmonic mean metric.
- `Accuracy` — range: [0, 1]
  - Proportion of correctly classified instances out of the total number of test instances.

## Input / output format

**Input**: Polish medical text snippets representing specific clinical scenarios.

**Output**: One of five clinical category labels per text instance.

## Scoring recipe

```python
def compute_metrics(predictions, gold_labels):
    accuracy = sum(p == g for p, g in zip(predictions, gold_labels)) / len(gold_labels)
    f1 = f1_score(gold_labels, predictions, average='macro')
    return {'accuracy': accuracy, 'f1': f1}
```

## Common pitfalls

- Metrics are reported per clinical scenario rather than globally aggregated across all categories.
- Ground truth is physician-validated rather than raw, limiting direct comparison with uncurated real-world benchmarks.
- The exact averaging strategy (macro vs. micro) for F1 is not explicitly stated in the text.

## Evidence (verbatim from paper)

> Finally, each trained BERT classifier was evaluated on the physician-validated test sets. DistilBERT achieves F1 scores >0.80 across all five clinical categories and >0.93 for three, outperforming others in accuracy while being 500× smaller and 300× more memory-efficient than the teacher LLM...

## Citation

```bibtex
@misc{gorski2025admedtagger,
  title={ADMEDTAGGER: an annotation framework for distillation of expert knowledge for the Polish medical language},
  author={Górski et al. (2025)},
  year={2025},
  note={arXiv:2601.09722}
}
```

- arXiv: 2601.09722

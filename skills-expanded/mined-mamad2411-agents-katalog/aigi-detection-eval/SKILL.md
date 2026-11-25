---
name: aigi-detection-eval
description: Evaluates the ability of models to distinguish real photographs from AI-generated images across diverse, out-of-distribution, and post-processed scenarios. It probes both low-level pixel artifact detection and high-level semantic consistency checking to measure real-world generalization. Use when the user wants to benchmark on Chameleon, WildRF, AIGI-Bench, Co-SPY-Bench (in-the-wild), BFree-Online, AIGI-Now, GenImage, DRCT-2M, AIGCDetectBenchmark, or asks about evaluating this task. Reports Balanced accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.06746
  bibtex_key: chen2025taskmodelalignment
  confidence: high
---

# aigi-detection-eval

> Task-Model Alignment: A Simple Path to Generalizable AI-Generated Image Detection — Chen et al. (2025) (arXiv:2512.06746, 2025)

## What this evaluates

Evaluates the ability of models to distinguish real photographs from AI-generated images across diverse, out-of-distribution, and post-processed scenarios. It probes both low-level pixel artifact detection and high-level semantic consistency checking to measure real-world generalization.

## Datasets

- **Chameleon** — total ?; splits: test (-1)
- **WildRF** — total ?; splits: test (-1)
- **AIGI-Bench** — total ?; splits: test (-1)
- **Co-SPY-Bench (in-the-wild)** — total ?; splits: test (-1)
- **BFree-Online** — total ?; splits: test (-1)
- **AIGI-Now** — total ?; splits: test (-1)
- **GenImage** — total ?; splits: test (-1)
- **DRCT-2M** — total ?; splits: test (-1)
- **AIGCDetectBenchmark** — total ?; splits: test (-1)

## Metrics

- `Balanced accuracy` **(primary)** — range: [0, 1]
  - Mean of the classification accuracies on real images and synthetic (AI-generated) images: (Accuracy_real + Accuracy_fake) / 2.

## Input / output format

**Input**: Single RGB image (real or AI-generated)

**Output**: Binary classification label: real or synthetic (AI-generated)

## Scoring recipe

```python
def balanced_accuracy(predictions, gold_labels):
    real_mask = gold_labels == 'real'
    fake_mask = gold_labels == 'synthetic'
    acc_real = (predictions[real_mask] == gold_labels[real_mask]).mean()
    acc_fake = (predictions[fake_mask] == gold_labels[fake_mask]).mean()
    return (acc_real + acc_fake) / 2
```

## Common pitfalls

- Baselines are evaluated using their officially released checkpoints without per-benchmark retuning, so direct comparison requires strict adherence to the same zero-shot evaluation protocol.
- The full CO-SPY-Bench/in-the-wild dataset is not publicly available due to licensing restrictions; evaluation uses a restricted subset provided by the authors, which may cause score discrepancies compared to original papers.
- Mixed supervision during training dilutes branch specialization, so task-pure supervision (semantic-only for VLM, artifact-only for expert) is critical for optimal performance.

## Evidence (verbatim from paper)

> Balanced accuracy is adopted as the primary metric, defined as the mean of the accuracies on real and synthetic images.

## Citation

```bibtex
@misc{chen2025taskmodelalignment,
  title={Task-Model Alignment: A Simple Path to Generalizable AI-Generated Image Detection},
  author={Chen et al. (2025)},
  year={2025},
  note={arXiv:2512.06746}
}
```

- arXiv: 2512.06746

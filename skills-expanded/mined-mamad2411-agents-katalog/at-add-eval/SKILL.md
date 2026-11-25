---
name: at-add-eval
description: This evaluation protocol probes the robustness and generalization of audio deepfake detectors under real-world distortions and across heterogeneous audio types. It specifically tests whether models can maintain reliable binary classification performance when facing unseen generation methods, recording condition shifts, and unknown audio categories without relying on type-specific labels. Use when the user wants to benchmark on AT-ADD Challenge Dataset, or asks about evaluating this task. Reports real/fake prediction.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.08184
  bibtex_key: xie2026atadd
  confidence: high
---

# at-add-eval

> AT-ADD: All-Type Audio Deepfake Detection Challenge Evaluation Plan — Xie et al. (2026) (arXiv:2604.08184, 2026)

## What this evaluates

This evaluation protocol probes the robustness and generalization of audio deepfake detectors under real-world distortions and across heterogeneous audio types. It specifically tests whether models can maintain reliable binary classification performance when facing unseen generation methods, recording condition shifts, and unknown audio categories without relying on type-specific labels.

## Datasets

- **AT-ADD Challenge Dataset** — total ?; splits: train (-1), development (-1), test (-1)

## Metrics

- `real/fake prediction` **(primary)** — range: [0, 1]
  - Standard binary classification accuracy: the proportion of correctly classified real vs. fake audio clips out of the total evaluation set. Calculated as (TP + TN) / (TP + TN + FP + FN).

## Input / output format

**Input**: Raw audio clip (speech utterance for Track 1; heterogeneous audio type for Track 2).

**Output**: Binary label indicating 'real' or 'fake'.

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- Using external training data is strictly forbidden under the closed challenge setting.
- Assuming audio-type labels (speech, singing, music, etc.) are available at test time in Track 2.
- Treating signal distortions (compression, resampling, pitch shifting) or replay attacks as changing the ground-truth real/fake label.

## Evidence (verbatim from paper)

> Given an input speech utterance, participants are required to predict whether the input is real or fake. In this task, fake refers specifically to deepfake speech generated using deep neural network-based methods, while real refers to non-deepfake speech. It should be noted that signal distortions or transformations, such as compression, resampling, speed perturbation, and pitch shifting, as well as replay-based attacks, do not change the original real/fake label in this task.

## Citation

```bibtex
@misc{xie2026atadd,
  title={AT-ADD: All-Type Audio Deepfake Detection Challenge Evaluation Plan},
  author={Xie et al. (2026)},
  year={2026},
  note={arXiv:2604.08184}
}
```

- arXiv: 2604.08184

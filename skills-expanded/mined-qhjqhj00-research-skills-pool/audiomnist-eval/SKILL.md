---
name: audiomnist-eval
description: Evaluates audio classification performance on spoken digits and speaker sex using raw waveforms and spectrograms, serving as a benchmark for explainable AI (XAI) methods in the audio domain. Use when the user wants to benchmark on AudioMNIST, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1807.03418
  bibtex_key: becker2018audiomnist
  confidence: high
---

# audiomnist-eval

> AudioMNIST: Exploring Explainable Artificial Intelligence for Audio Analysis on a Simple Benchmark — Becker et al. (2018) (arXiv:1807.03418, 2018)

## What this evaluates

Evaluates audio classification performance on spoken digits and speaker sex using raw waveforms and spectrograms, serving as a benchmark for explainable AI (XAI) methods in the audio domain.

## Datasets

- **AudioMNIST** — total 30000; splits: test (-1); repo https://github.com/soerenab/AudioMNIST

## Metrics

- `accuracy` **(primary)** — range: percent
  - Standard classification accuracy: the proportion of correctly predicted labels out of the total number of instances, reported as mean ± standard deviation across test folds.

## Input / output format

**Input**: Raw waveform (1D, 8000-dimensional vector after downsampling to 8kHz and zero-padding) or spectrogram (2D, 227x227 frequency-time matrix converted to decibels).

**Output**: Discrete class label (digit 0-9 or speaker sex: male/female).

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    return (correct / len(gold)) * 100
```

## Common pitfalls

- The exact train/validation/test split protocol is not explicitly detailed in the text, only 'test folds' and 'data splits' are mentioned.
- Models use different architectures (AlexNet vs custom AudioNet) and input representations, so direct accuracy comparisons between them are cautioned against by the authors.

## Evidence (verbatim from paper)

> Model performances are summarized in Table 1 in terms of means and standard deviations across test folds. ... After the data has been manipulated as described, the trained network reaches an accuracy of only 20.3%±12.6% across test splits on the manipulated data, which is well-below chance level for this task.

## Citation

```bibtex
@misc{becker2018audiomnist,
  title={AudioMNIST: Exploring Explainable Artificial Intelligence for Audio Analysis on a Simple Benchmark},
  author={Becker et al. (2018)},
  year={2018},
  note={arXiv:1807.03418}
}
```

- arXiv: 1807.03418

---
name: audio-deepfake-generalization-eval
description: This benchmark evaluates the generalization capability of audio deepfake detection models by testing their performance on controlled, studio-recorded spoofing data versus real-world, uncontrolled in-the-wild audio. It probes whether models trained on standard lab benchmarks can robustly distinguish real from synthetic speech in practical deployment scenarios. Use when the user wants to benchmark on ASVspoof 2019 LA, In-the-Wild Data, or asks about evaluating this task. Reports EER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2203.16263
  bibtex_key: muller2022doesaudio
  confidence: high
---

# audio-deepfake-generalization-eval

> Does Audio Deepfake Detection Generalize? — Müller et al. (2022) (arXiv:2203.16263, 2022)

## What this evaluates

This benchmark evaluates the generalization capability of audio deepfake detection models by testing their performance on controlled, studio-recorded spoofing data versus real-world, uncontrolled in-the-wild audio. It probes whether models trained on standard lab benchmarks can robustly distinguish real from synthetic speech in practical deployment scenarios.

## Datasets

- **ASVspoof 2019 LA** — total ?; splits: train (-1), dev (-1), eval (-1)
- **In-the-Wild Data** — total ?; splits: test (-1)

## Metrics

- `EER` **(primary)** — range: percent
  - Equal Error Rate, the operating point where the False Acceptance Rate (FAR) equals the False Rejection Rate (FRR). Reported as a percentage.
- `t-DCF` — range: [0, 1]
  - Tandem Detection Cost Function, a cost metric that combines the costs of spoof detection errors and automatic speaker verification (ASV) errors, weighted by specific false alarm and miss costs defined in the ASVspoof challenge.

## Input / output format

**Input**: Audio samples provided either as raw waveforms or pre-extracted 513-dimensional features (cqtspec, logspec, melspec). Inputs are processed as either full variable-length recordings or fixed 4-second segments (randomly sampled if longer, repeated if shorter).

**Output**: A binary classification probability or logit indicating whether the input audio is real or spoofed/deepfake.

## Scoring recipe

```python
def compute_eer(predictions, labels):
    # predictions: continuous scores, labels: 0 (real) or 1 (fake)
    far, frr, thresholds = compute_roc(predictions, labels)
    # Find threshold where FAR ≈ FRR
    idx = np.argmin(np.abs(far - frr))
    eer = (far[idx] + frr[idx]) / 2.0
    return eer * 100  # Return as percentage
```

## Common pitfalls

- Evaluating solely on the ASVspoof 2019 'eval' split overestimates real-world robustness because the test audios share acoustic properties with the training data.
- Using mel-scaled spectrograms (melspec) instead of cqtspec or logspec features causes severe performance degradation (up to 37% EER drop on average).
- Fixed 4-second truncation/repetition strategies can unfairly penalize models that naturally handle variable-length inputs, skewing cross-architecture comparisons.

## Evidence (verbatim from paper)

> We report both the equal-error rate (EER) and the tandem detection cost function (t-DCF) on the ASVspoof 2019 ‘eval’ data. For consistency with the related work, we use the original implementation of the t-DCF as provided for the ASVspoof 2019 challenge. For our proposed dataset, we report only the EER. This is because t-DCF scores require the false alarm and miss costs, which are available only for ASVspoof.

## Citation

```bibtex
@misc{muller2022doesaudio,
  title={Does Audio Deepfake Detection Generalize?},
  author={Müller et al. (2022)},
  year={2022},
  note={arXiv:2203.16263}
}
```

- arXiv: 2203.16263

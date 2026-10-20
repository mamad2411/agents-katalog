---
name: avse-cog-mhear-eval
description: Evaluates audio-visual speech enhancement models on their ability to suppress background noise and competing speakers while preserving speech intelligibility and perceptual quality in real-time hearing aid scenarios. Use when the user wants to benchmark on COG-MHEAR AVSE Challenge, or asks about evaluating this task. Reports PESQ.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.19483
  bibtex_key: saleem2025audiovisual
  confidence: high
---

# avse-cog-mhear-eval

> Audio-Visual Feature Synchronization for Robust Speech Enhancement in Hearing Aids — Saleem et al. (2025) (arXiv:2508.19483, 2025)

## What this evaluates

Evaluates audio-visual speech enhancement models on their ability to suppress background noise and competing speakers while preserving speech intelligibility and perceptual quality in real-time hearing aid scenarios.

## Datasets

- **COG-MHEAR AVSE Challenge** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `PESQ` **(primary)** — range: other
  - ITU-T P.862 standard metric that compares enhanced speech to a clean reference, scoring perceptual quality from -0.5 (poor) to 4.5 (excellent). Higher values indicate better quality.
- `STOI` — range: [0, 1]
  - Short-Time Objective Intelligibility measures the correlation between time-frequency envelopes of enhanced and clean signals. Scores range from 0 (unintelligible) to 1 (fully intelligible).
- `SI-SDR` — range: other
  - Scale-Invariant Signal-to-Distortion Ratio computes the logarithmic energy ratio between target speech and residual distortion, invariant to scale differences. Formula: 10*log10(||x||^2 / ||x-x_hat||^2). Higher values (in dB) indicate better fidelity.

## Input / output format

**Input**: Monaural audio clips sampled at 16 kHz paired with corresponding video frames (128x128 pixels) of a single speaker, mixed with background noise or competing speech at varying SNRs (-15dB to 10dB).

**Output**: Enhanced monaural audio waveform (estimated clean speech signal).

## Scoring recipe

```python
def compute_metrics(y_true, y_pred):
    pesq_score = pesq(y_true, y_pred, fs=16000)  # ITU-T P.862, range [-0.5, 4.5]
    stoi_score = stoi(y_true, y_pred, fs=16000)  # envelope correlation, range [0, 1]
    # SI-SDR: 10 * log10(||x||^2 / ||x - x_hat||^2)
    sdr_db = 10 * np.log10(np.sum(y_true**2) / np.sum((y_true - y_pred)**2))
    return {'PESQ': pesq_score, 'STOI': stoi_score, 'SI-SDR': sdr_db}
```

## Common pitfalls

- SI-SDR is scale-invariant, meaning amplitude scaling of the enhanced output does not penalize the score, which can mask clipping or gain issues.
- PESQ internally resamples to 8 kHz and uses a specific perceptual model; direct comparison with other metrics requires careful handling of sampling rates and alignment.
- STOI operates on time-frequency envelopes, so it may not capture phase distortions or fine spectral details that affect perceived quality.

## Evidence (verbatim from paper)

> The quality of the enhanced speech is evaluated using three standard metrics: Perceptual Evaluation of Speech Quality (PESQ) [[17]], Short-Time Objective Intelligibility (STOI) [[18]], and scale-invariant signal-to-distortion ratio (SI-SDR) [[19]]. PESQ (ITU-T P.862) evaluates speech quality by comparing the enhanced signal to the clean reference signal, providing a score ranging from -0.5 (poor) to 4.5 (excellent), with higher values indicating better perceptual quality. STOI predicts speech intelligibility by measuring the correlation between the time-frequency envelopes of the enhanced and clean signals, yielding a value between 0 (unintelligible) and 1 (fully intelligible).

## Citation

```bibtex
@misc{saleem2025audiovisual,
  title={Audio-Visual Feature Synchronization for Robust Speech Enhancement in Hearing Aids},
  author={Saleem et al. (2025)},
  year={2025},
  note={arXiv:2508.19483}
}
```

- arXiv: 2508.19483

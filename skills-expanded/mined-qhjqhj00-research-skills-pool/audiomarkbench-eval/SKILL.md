---
name: audiomarkbench-eval
description: Evaluates the robustness of audio watermarking detectors against watermark removal and forgery under no-box, black-box, and white-box threat models. It also measures the perceptual and signal quality of perturbed audio to ensure attacks do not excessively degrade the host signal. Use when the user wants to benchmark on AudioMarkData, LibriSpeech, or asks about evaluating this task. Reports FNR, FPR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2406.06979
  bibtex_key: liu2024audiomarkbench
  confidence: high
---

# audiomarkbench-eval

> AudioMarkBench: Benchmarking Robustness of Audio Watermarking — Liu et al. (2024) (arXiv:2406.06979, 2024)

## What this evaluates

Evaluates the robustness of audio watermarking detectors against watermark removal and forgery under no-box, black-box, and white-box threat models. It also measures the perceptual and signal quality of perturbed audio to ensure attacks do not excessively degrade the host signal.

## Datasets

- **AudioMarkData** — total ?; splits: test (-1); repo https://github.com/moyangkuo/AudioMarkBench
- **LibriSpeech** — total ?; splits: test (-1)

## Metrics

- `FNR` **(primary)** — range: [0, 1]
  - False Negative Rate: the fraction of watermarked audios that are incorrectly detected as unwatermarked. Lower values indicate better robustness to watermark removal.
- `FPR` **(primary)** — range: [0, 1]
  - False Positive Rate: the fraction of unwatermarked audios that are incorrectly detected as watermarked. Lower values indicate better robustness to watermark forgery.
- `SNR` — range: other
  - Signal-to-Noise Ratio: compares the noise level of a perturbed audio to its clean reference audio. Higher values indicate clearer audio.
- `ViSQOL` — range: [1, 5]
  - Perceptual audio quality score simulating human hearing. Ranges from 1 to 5, where higher scores indicate better quality preservation. Scores ≥ 3 reflect good quality.

## Input / output format

**Input**: Watermarked or unwatermarked audio samples, optionally subjected to no-box, black-box, or white-box perturbations (e.g., MP3 compression, noise, adversarial attacks).

**Output**: Continuous detection score/logit from the watermarking model, compared against a dataset- and method-specific threshold τ to yield a binary detection decision (watermarked vs. unwatermarked).

## Scoring recipe

```python
def compute_fnr(predictions, gold, threshold):
    watermarked = [p for p, g in zip(predictions, gold) if g == 1]
    fns = sum(1 for p in watermarked if p < threshold)
    return fns / len(watermarked) if watermarked else 0.0

def compute_fpr(predictions, gold, threshold):
    unwatermarked = [p for p, g in zip(predictions, gold) if g == 0]
    fps = sum(1 for p in unwatermarked if p >= threshold)
    return fps / len(unwatermarked) if unwatermarked else 0.0

# Note: threshold τ is calibrated per method/dataset to achieve FPR, FNR < 0.01 before robustness testing.
```

## Common pitfalls

- The detection threshold τ is not fixed globally; it must be calibrated per watermarking method and dataset to balance FPR and FNR (typically <0.01) before evaluating perturbation robustness.
- ViSQOL is strongly preferred over SNR for assessing audio quality preservation, as SNR does not correlate well with human perception and can be misleading.
- Black-box and white-box attacks assume access to the detector API or model weights, which drastically changes the threat model compared to no-box perturbations and requires careful query budgeting.

## Evidence (verbatim from paper)

> We use FNR and FPR to evaluate the robustness of audio watermarking. Specifically, FNR/FPR is the fraction of watermarked/unwatermarked audios that are incorrectly detected as unwatermarked/watermarked. Lower FNR/FPR indicate better audio watermarking methods. When watermarked audios (or unwatermarked audios) are modified by watermark-removal (or watermark-forgery) perturbations, lower FNR (or FPR) indicates that the watermarking method is more robust against watermark removal (or watermark forgery).

## Citation

```bibtex
@misc{liu2024audiomarkbench,
  title={AudioMarkBench: Benchmarking Robustness of Audio Watermarking},
  author={Liu et al. (2024)},
  year={2024},
  note={arXiv:2406.06979}
}
```

- arXiv: 2406.06979

---
name: audio-visual-separation-eval
description: This protocol evaluates an audio-visual model's ability to isolate and separate target instrument sounds from mixed multi-source video audio using visual object cues. It quantifies separation accuracy and artifact suppression across held-out test clips and synthetically mixed pairs. The evaluation also probes generalization to unseen object combinations and visually-guided denoising on real-world videos. Use when the user wants to benchmark on MUSIC, AudioSet-Unlabeled, AudioSet-SingleSource, AV-Bench, or asks about evaluating this task. Reports SDR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1904.07750
  bibtex_key: gao2019coseparating
  confidence: high
---

# audio-visual-separation-eval

> Co-Separating Sounds of Visual Objects — Gao et al. (2019) (arXiv:1904.07750, 2019)

## What this evaluates

This protocol evaluates an audio-visual model's ability to isolate and separate target instrument sounds from mixed multi-source video audio using visual object cues. It quantifies separation accuracy and artifact suppression across held-out test clips and synthetically mixed pairs. The evaluation also probes generalization to unseen object combinations and visually-guided denoising on real-world videos.

## Datasets

- **MUSIC** — total 9456; splits: train (8928), val (259), test (269)
- **AudioSet-Unlabeled** — total 113756; splits: train (113756)
- **AudioSet-SingleSource** — total 15; splits: test (15)
- **AV-Bench** — total 3; splits: test (3)

## Metrics

- `SDR` **(primary)** — range: dB
  - Signal-to-Distortion Ratio (SDR) measures the overall quality of the separated signal relative to the reference, capturing both interference and artifacts. Reported in decibels (dB).
- `SIR` — range: dB
  - Signal-to-Interference Ratio (SIR) quantifies how well interfering sources are suppressed relative to the target signal. Reported in decibels (dB).
- `SAR` — range: dB
  - Signal-to-Artifact Ratio (SAR) measures the absence of artifacts introduced by the separation process, independent of separation accuracy. Reported in decibels (dB).

## Input / output format

**Input**: 6-second audio clips (sub-sampled at 11kHz) converted to 256x256 log-frequency magnitude spectrograms, paired with visual object crops (224x224) or scene images.

**Output**: Separated magnitude spectrograms (or time-domain audio waveforms) corresponding to each target visual object/source.

## Scoring recipe

```python
import mir_eval
import numpy as np

def compute_metrics(pred_audio, ref_audio):
    # mir_eval expects 2D arrays of shape (n_sources, n_samples)
    ref = np.array([ref_audio])
    pred = np.array([pred_audio])
    sdr, sir, sar, _ = mir_eval.separation.bss_eval_sources(
        reference=ref, estimated=pred, compute_permutation=False
    )
    return sdr[0, 0], sir[0, 0], sar[0, 0]

# Average across all test clips to report final metric values.
```

## Common pitfalls

- SAR measures artifacts, not separation accuracy; naively copying the input twice yields high SAR (~80 dB), so relying solely on SAR is misleading.
- Test evaluation relies on synthetically mixing two single-source videos to guarantee ground truth, which differs from real multi-source audio complexity.
- For ungrounded baselines like NMF-MFCC, both possible source-to-target matchings must be evaluated and the best score reported, artificially inflating results.

## Evidence (verbatim from paper)

> We use the widely used mir eval library to evaluate the source separation and report the standard metrics: Signal-to-Distortion Ration (SDR), Signal-to-Interference Ratio (SIR), and Signal-to-Artifact Ratio (SAR).

## Citation

```bibtex
@misc{gao2019coseparating,
  title={Co-Separating Sounds of Visual Objects},
  author={Gao et al. (2019)},
  year={2019},
  note={arXiv:1904.07750}
}
```

- arXiv: 1904.07750

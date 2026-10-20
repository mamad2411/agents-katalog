---
name: audio-source-separation-eval
description: Evaluates an audio-only model's ability to disentangle and reconstruct individual sound sources from mixed audio using semantic category guidance, without relying on visual cues. Use when the user wants to benchmark on MUSIC, FUSS, MUSDB18, VGG-Sound, or asks about evaluating this task. Reports SDR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.03736
  bibtex_key: mo2024sgn
  confidence: high
---

# audio-source-separation-eval

> Semantic Grouping Network for Audio Source Separation — Mo et al. (2024) (arXiv:2407.03736, 2024)

## What this evaluates

Evaluates an audio-only model's ability to disentangle and reconstruct individual sound sources from mixed audio using semantic category guidance, without relying on visual cues.

## Datasets

- **MUSIC** — total 448; splits: train (358), test (90)
- **FUSS** — total 22000; splits: train (20000), val (1000), test (1000)
- **MUSDB18** — total 50; splits: test (50)
- **VGG-Sound** — total 150000; splits: test (150000)

## Metrics

- `SDR` **(primary)** — range: other
  - Signal-to-Distortion Ratio. Measures the ratio of target source energy to total distortion energy (including interference, artifacts, and noise).
- `SI-SDR` — range: other
  - Scale-invariant SDR. Computes SDR after optimally scaling the estimated source to match the reference, removing gain-dependent bias.
- `SIR` — range: other
  - Signal-to-Interference Ratio. Measures the ratio of target source energy to interference energy from other sources.
- `SAR` — range: other
  - Signal-to-Artifact Ratio. Measures the ratio of target source energy to artifact energy (non-linear distortions and noise).

## Input / output format

**Input**: Log-frequency audio mixture spectrogram of shape 256×256, derived from 11kHz sub-sampled audio via STFT (window 1022, hop 256).

**Output**: Reconstructed category-aware spectrograms of shape 65536×256 (reshaped to 256×256), one per source class.

## Scoring recipe

```python
import mir_eval
import numpy as np

def compute_metrics(references, estimates):
    # references, estimates: (n_sources, n_samples) arrays
    sdr, sir, sar, si_sdr = mir_eval.separation.bss_eval_sources(
        references, estimates, compute_permutation=False, zero_mean=True
    )
    return {
        'SDR': float(np.mean(sdr)),
        'SIR': float(np.mean(sir)),
        'SAR': float(np.mean(sar)),
        'SI-SDR': float(np.mean(si_sdr))
    }
```

## Common pitfalls

- Using the original MUSIC dataset instead of the filtered version specified in the footnote, which breaks fair comparison with baselines.
- Confusing audio-only baselines with audio-visual ones; the paper emphasizes that SGN matches/exceeds audio-visual methods without visual cues.
- Metrics are computed via mir_eval; using different BSS evaluation implementations can yield slight numerical discrepancies.

## Evidence (verbatim from paper)

> Datasets. MUSIC [13] contains 448 untrimmed YouTube music videos of solos and duets from 11 instrument categories. 358 solo videos are applied for training, and 90 solo videos for evaluation. FUSS [11] is a universal sound dataset with 10 second clips from FSD50K [73] with annotated labels from the AudioSet Ontology, which includes between 1 and 4 sound sources. The number of available categories is 286. We use 20000 mixture clips for training, 1000 mixture clips for validation, and 1000 mixture clips for testing. ... Evaluation Metrics. Following previous work [8], [9], [13], [74], we use scale-invariant SDR (SI-SDR), Signal-to-Distortion Ratio (SDR), Signal-to-Interference Ratio (SIR), and Signal-to-Artifact Ratio (SAR) to evaluate the separation performance. The open-source mir_eval [75] library is utilized for computing the results to report.

## Citation

```bibtex
@misc{mo2024sgn,
  title={Semantic Grouping Network for Audio Source Separation},
  author={Mo et al. (2024)},
  year={2024},
  note={arXiv:2407.03736}
}
```

- arXiv: 2407.03736

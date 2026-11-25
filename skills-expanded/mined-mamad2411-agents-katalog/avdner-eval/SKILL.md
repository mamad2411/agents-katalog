---
name: avdner-eval
description: Evaluates the ability of audio-visual models to separate cinematic audio into speech, music, and sound effects using visual cues like lip movements and scene context. It probes cross-track isolation, perceptual fidelity, and the model's capacity to leverage multi-stream video information for source disentanglement. Use when the user wants to benchmark on AVDnR, or asks about evaluating this task. Reports FAD.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.26113
  bibtex_key: zhang2026cinematic
  confidence: high
---

# avdner-eval

> Cinematic Audio Source Separation Using Visual Cues — Zhang et al. (2026) (arXiv:2603.26113, 2026)

## What this evaluates

Evaluates the ability of audio-visual models to separate cinematic audio into speech, music, and sound effects using visual cues like lip movements and scene context. It probes cross-track isolation, perceptual fidelity, and the model's capacity to leverage multi-stream video information for source disentanglement.

## Datasets

- **AVDnR** — total 1000; splits: test (1000)

## Metrics

- `FAD` **(primary)** — range: other
  - Fréchet Audio Distance measures the distributional similarity between generated and real audio embeddings. Computed as the Fréchet distance between multivariate Gaussians fitted to feature distributions of real and predicted audio. Lower is better.
- `SI-SDRi` — range: other
  - Scale-Invariant Signal-to-Distortion Ratio improvement. Measures the ratio of target signal power to residual error power, scaled to be invariant to amplitude differences. Reported in dB. Higher is better.
- `PESQ` — range: other
  - Perceptual Evaluation of Speech Quality. A standardized ITU-T metric that predicts subjective speech quality by comparing enhanced speech to a clean reference. Evaluated only on the speech stem. Higher is better.
- `WPR` — range: percent
  - Wrong Placement Ratio. Estimates the proportion of residual or misplaced components from other stems using a pretrained sound event detection model (PANNs). Computed at the stem level without ground-truth references. Lower is better.
- `MOS` — range: other
  - Mean Opinion Score. Subjective rating on a 5-point Likert scale (1=Poor, 5=Excellent) based on clarity of separation and completeness of target reconstruction. Higher is better.

## Input / output format

**Input**: Paired audio spectrogram and video frames (facial and scene streams). For audio-only evaluation, only the audio spectrogram is provided.

**Output**: Three separated audio stems: dialogue (speech), music, and sound effects.

## Scoring recipe

```python
def compute_metrics(pred_stems, gt_stems=None, video=None):
    # WPR: stem-level isolation using PANNs
    wpr_scores = []
    for stem in ['speech', 'music', 'fx']:
        misplaced = panns_detect(pred_stems[stem], exclude_class=stem)
        wpr_scores.append(len(misplaced) / total_segments)
    wpr = sum(wpr_scores) / 3
    
    # FAD & KL: dataset-level distributional similarity
    fad = frechet_audio_distance(gt_stems, pred_stems)
    kl = kl_divergence(gt_stems, pred_stems)
    
    # SI-SDRi & PESQ: instance-level reconstruction/quality
    sdr = scale_invariant_sdr(gt_stems, pred_stems)
    pesq = perceptual_speech_quality(gt_stems['speech'], pred_stems['speech'])
    
    return {'FAD': fad, 'KL': kl, 'SI-SDRi': sdr, 'PESQ': pesq, 'WPR': wpr}
```

## Common pitfalls

- Real-world samples lack ground-truth stems, requiring subjective MOS or proxy metrics like WPR instead of direct reconstruction error.
- FAD and KL measure dataset-level distributional similarity, not per-instance accuracy, so they can mask individual failure cases.
- WPR relies on PANNs (a sound event detector) and may misclassify overlapping or rare cinematic sounds, affecting stem-level isolation scores.

## Evidence (verbatim from paper)

> We use Fréchet Audio Distance (FAD) and Kullback-Leibler divergence (KL) from AudioLDM to measure distributional similarity between generated and real audio. We also report Perceptual Evaluation of Speech Quality (PESQ) for speech and Scale-Invariant Signal-to-Distortion Ratio improvement (SI-SDRi) in dB, following prior works. For FAD, KL, and SI-SDRi, we report averages across all three sources. In addition, we introduce a new metric, Wrong Placement Ratio (WPR), to estimate the proportion of residual or misplaced components from other stems.

## Citation

```bibtex
@misc{zhang2026cinematic,
  title={Cinematic Audio Source Separation Using Visual Cues},
  author={Zhang et al. (2026)},
  year={2026},
  note={arXiv:2603.26113}
}
```

- arXiv: 2603.26113

---
name: TTSDS
description: Measures the distributional distance between synthetic and real speech across five key factors: environment, speaker identity, prosody, intelligibility, and general speech distribution. It evaluates TTS system quality without relying on subjective Mean Opinion Scores (MOS) or simple mean-based metrics. Use when the user has predictions and gold and needs to compute TTSDS.
metadata:
  skill_kind: metric
  source_arxiv: 2407.12707
  bibtex_key: minixhofer2024ttsds
  confidence: high
---

# TTSDS

> TTSDS -- Text-to-Speech Distribution Score — Minixhofer et al. (2024) (arXiv:2407.12707, 2024)

## What this evaluates

Measures the distributional distance between synthetic and real speech across five key factors: environment, speaker identity, prosody, intelligibility, and general speech distribution. It evaluates TTS system quality without relying on subjective Mean Opinion Scores (MOS) or simple mean-based metrics.

## Datasets

- **LibriTTS** — total ?; splits: test (-1)
- **LJSpeech** — total ?; splits: test (-1)
- **VCTK** — total ?; splits: test (-1)
- **ESC** — total ?; splits: test (-1)
- **Blizzard Challenge Training Sets (2008, 2013, 2021)** — total ?; splits: train (-1)

## Metrics

- `TTSDS` **(primary)** — range: other
  - Computes distributional distances between synthetic and reference speech using high-dimensional embeddings (e.g., HuBERT, wav2vec 2.0) and scalar features (e.g., pitch, WER, SNR). Features are averaged per factor (environment, speaker identity, prosody, intelligibility, general speech), and factor scores are averaged to produce the final TTSDS score.

## Input / output format

**Input**: Synthetic TTS audio, reference audio, and text transcripts. Conditioning uses speaker reference waveforms from LibriTTS test set paired with unrelated transcripts.

**Output**: Scalar TTSDS score and per-factor scores (environment, speaker identity, prosody, intelligibility, general speech).

## Scoring recipe

```python
# Compute per-factor distributional distances using embeddings/scalar features
factor_scores = {}
for factor in [environment, speaker, prosody, intelligibility, general]:
    distances = compute_distribution_distance(synthetic_features[factor], reference_features[factor])
    factor_scores[factor] = mean(distances)

# Average factor scores to get final metric
ttsds_score = mean(list(factor_scores.values()))
```

## Common pitfalls

- Relies on non-public TTS systems (e.g., TTS Arena) requiring dataset reproduction.
- Uses unrelated transcripts paired with reference speakers to prevent model memorization during generation.
- Distribution-based approach avoids pitfalls of mean-based metrics that mask intra-sample variability.

## Evidence (verbatim from paper)

> For all system $	imes$ feature combinations, we compute the score as described in Section 2.4. We average all features for each factor, which gives us the corresponding factor score. Averaging all factor scores in turn gives the TTSDS score.

## Citation

```bibtex
@misc{minixhofer2024ttsds,
  title={TTSDS -- Text-to-Speech Distribution Score},
  author={Minixhofer et al. (2024)},
  year={2024},
  note={arXiv:2407.12707}
}
```

- arXiv: 2407.12707

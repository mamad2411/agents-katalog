---
name: adept-prosody-clone-eval
description: Evaluates a zero-shot multispeaker TTS model's ability to clone both speaker voice and fine-grained prosody from untranscribed reference audio. It measures intelligibility, spectral/prosodic fidelity, and perceptual similarity against human references. Use when the user wants to benchmark on ADEPT, or asks about evaluating this task. Reports Phone Error Rate (PER).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2206.12229
  bibtex_key: lux2022exactprosody
  confidence: high
---

# adept-prosody-clone-eval

> Exact Prosody Cloning in Zero-Shot Multispeaker Text-to-Speech — Lux et al. (2022) (arXiv:2206.12229, 2022)

## What this evaluates

Evaluates a zero-shot multispeaker TTS model's ability to clone both speaker voice and fine-grained prosody from untranscribed reference audio. It measures intelligibility, spectral/prosodic fidelity, and perceptual similarity against human references.

## Datasets

- **ADEPT** — total ?; splits: test (-1)

## Metrics

- `Phone Error Rate (PER)` **(primary)** — range: percent
  - Phone error rate computed by an ASR system on synthetic speech compared to the ground truth text. Lower values indicate higher intelligibility.
- `Mel Spectral Distortion (MSD)` — range: other
  - DTW of the sum of Euclidean distances between log mel spectrogram frames, divided by the total number of timesteps in the reference sequence: MSD(x,y) = DTW(sum(dist(x_t1, y_t2))) / T_x.
- `F0 Frame Error (FFE)` — range: percent
  - Normalized count of voicing decision errors (VDE) and gross pitch errors (GPE) across timesteps: FFE(x,y) = (VDE + GPE) / T_x. GPE counts frames where pitch deviates outside the [0.8, 1.2] factor of the reference.
- `Speaker Similarity` — range: [-1, 1]
  - Cosine similarity between speaker embeddings extracted from the reference audio and the synthetic audio.

## Input / output format

**Input**: Reference audio clip (untranscribed) and target text sequence.

**Output**: Synthesized audio waveform.

## Scoring recipe

```python
def compute_msd(x, y):
    # x, y: log mel spectrograms
    dist_mat = euclidean_dist_matrix(x, y)
    dtw_cost = dtw_min_path_sum(dist_mat)
    return dtw_cost / len(x)

def compute_ffe(x, y):
    # x, y: pitch contours (0 for unvoiced)
    vde = sum(1 for t in range(len(x)) if (x[t]==0) != (y[t]==0))
    gpe = sum(1 for t in range(len(x)) if not (0.8*x[t] <= y[t] <= 1.2*x[t]))
    return (vde + gpe) / len(x)
```

## Common pitfalls

- The authors explicitly skipped the official ADEPT benchmark tasks due to lack of human evaluation capacity, so results are not directly comparable to the official leaderboard.
- FFE uses a strict 20% tolerance window (0.8 to 1.2) for pitch matching, which differs from standard F0 error metrics that often use absolute Hz thresholds.
- MSD requires Dynamic Time Warping (DTW) alignment before distance calculation, making it computationally expensive and sensitive to sequence length normalization.

## Evidence (verbatim from paper)

> In order to measure whether the cloning of the prosody or the cloning of the voice alone or in conjunction affect the quality of the synthetic audio, we use an ASR system to measure the intelligibility by calculating the Phone Error Rate (PER) that the ASR achieves on synthetic speech produced using different configurations and compare it to the PER on human speech. For the ASR we use the architecture described in [[43]] and the English recipe from the IMS-speech resource [[44]]. We use Mel Spectral Distortion (MSD), which is a derivation of Mel Cepstral Distortion [[45]] with Dynamic Time Warping (DTW) [[46]] and the F0 Frame Error (FFE) [[47]] to asses the effectiveness of style cloning when using the same voice as suggested in [[11]].

## Citation

```bibtex
@misc{lux2022exactprosody,
  title={Exact Prosody Cloning in Zero-Shot Multispeaker Text-to-Speech},
  author={Lux et al. (2022)},
  year={2022},
  note={arXiv:2206.12229}
}
```

- arXiv: 2206.12229

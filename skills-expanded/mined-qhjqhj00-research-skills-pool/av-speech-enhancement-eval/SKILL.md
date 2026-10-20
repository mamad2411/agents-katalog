---
name: av-speech-enhancement-eval
description: This benchmark evaluates a model's ability to isolate a target speaker's voice from multi-talker audio environments using only lip-region video inputs. It probes audio-visual speech enhancement, testing how well the network predicts magnitude and phase masks to suppress interference and noise while preserving speech intelligibility and perceptual quality. Use when the user wants to benchmark on LRS2, VoxCeleb2, or asks about evaluating this task. Reports PESQ.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1804.04121
  bibtex_key: afouras2018conversation
  confidence: high
---

# av-speech-enhancement-eval

> The Conversation: Deep Audio-Visual Speech Enhancement — Afouras et al. (2018) (arXiv:1804.04121, 2018)

## What this evaluates

This benchmark evaluates a model's ability to isolate a target speaker's voice from multi-talker audio environments using only lip-region video inputs. It probes audio-visual speech enhancement, testing how well the network predicts magnitude and phase masks to suppress interference and noise while preserving speech intelligibility and perceptual quality.

## Datasets

- **LRS2** — total ?; splits: train (-1), test (-1)
- **VoxCeleb2** — total ?; splits: train (-1), test (-1)

## Metrics

- `SIR` — range: dB
  - Signal to Interference Ratio; measures how well unwanted signals (interference from other speakers) are suppressed relative to the target signal.
- `SDR` — range: dB
  - Signal to Distortion Ratio; an overall quality measure that accounts for both interference suppression and introduced artifacts.
- `PESQ` **(primary)** — range: [0, 4.5]
  - Perceptual Evaluation of Speech Quality; measures overall perceptual quality and correlates best with listening tests accounting for phase distortion.
- `WER` — range: percent
  - Word Error Rate; computed using an off-the-shelf ASR system (Google Speech Recognition) on enhanced audio, measuring speech intelligibility.
- `SAR` — range: dB
  - Signal to Artefacts Ratio; accounts for artifacts introduced by the enhancement process.
- `STOI` — range: [0, 1]
  - Short-Time Objective Intelligibility; correlates with the intelligibility of the enhanced speech signal.

## Input / output format

**Input**: Lip-region video frames (processed into visual features via a pre-trained front-end) and mixed audio spectrograms (magnitude and phase) containing a target speaker plus 1-4 interfering speakers.

**Output**: Enhanced audio spectrograms (predicted magnitude and phase), which are converted back to time-domain waveforms for metric computation.

## Scoring recipe

```python
def scoring_recipe(predictions, gold):
    # predictions and gold are time-domain audio waveforms
    sir = compute_sir(predictions, gold)
    sdr = compute_sdr(predictions, gold)
    sar = compute_sar(predictions, gold)
    pesq = compute_pesq(predictions, gold)
    wer = compute_wer_asr(predictions)
    return {'SIR': sir, 'SDR': sdr, 'SAR': sar, 'PESQ': pesq, 'WER': wer}
```

## Common pitfalls

- Phase prediction is notoriously difficult; using approximated phases (e.g., Griffin-Lim) or mixed phases significantly degrades perceptual quality and WER compared to ground truth phase.
- Audio-video synchronization is critical; the model is highly sensitive to temporal misalignment between lip movements and speech, requiring preprocessing pipelines for real-world videos.
- WER evaluation relies on a specific off-the-shelf ASR system (Google Speech Recognition), so results may not generalize to other ASR backbones or languages not covered by the ASR.

## Evidence (verbatim from paper)

> We evaluate the enhancement performance of the model in terms of perceptual speech quality using the blind source separation criteria described in[42]... The Signal to Interference Ratio (SIR) measures how well the unwanted signals have been suppressed, the Signal to Artefacts Ratio (SAR) accounts for the introduction of artefacts by the enhancement process, and the Signal to Distortion Ratio (SDR) is an overall quality measure, taking both into account. We also report results on PESQ [44], which measures the overall perceptual quality and STOI [45], which is correlated with the intelligibility of the signal.

## Citation

```bibtex
@misc{afouras2018conversation,
  title={The Conversation: Deep Audio-Visual Speech Enhancement},
  author={Afouras et al. (2018)},
  year={2018},
  note={arXiv:1804.04121}
}
```

- arXiv: 1804.04121

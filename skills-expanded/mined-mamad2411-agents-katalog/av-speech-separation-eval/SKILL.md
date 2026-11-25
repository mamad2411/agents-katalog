---
name: av-speech-separation-eval
description: Evaluates a model's ability to separate target speaker speech from audio mixtures (noise or other speakers) using synchronized visual face cues. It probes speaker-independent audio-visual fusion and robustness to varying numbers of speakers and background noise. Use when the user wants to benchmark on AVSpeech, AudioSet, CHiME-2, Mandarin, TCD-TIMIT, CUAVE, or asks about evaluating this task. Reports SDR improvement.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1804.03619
  bibtex_key: ephrat2018looking
  confidence: high
---

# av-speech-separation-eval

> Looking to Listen at the Cocktail Party: A Speaker-Independent Audio-Visual Model for Speech Separation — Ephrat et al. (2018) (arXiv:1804.03619, 2018)

## What this evaluates

Evaluates a model's ability to separate target speaker speech from audio mixtures (noise or other speakers) using synchronized visual face cues. It probes speaker-independent audio-visual fusion and robustness to varying numbers of speakers and background noise.

## Datasets

- **AVSpeech** — total ?; splits: train (-1), test (-1)
- **AudioSet** — total ?; splits: train (-1), test (-1)
- **CHiME-2** — total ?; splits: test (-1)
- **Mandarin** — total ?; splits: test (-1)
- **TCD-TIMIT** — total ?; splits: test (-1)
- **CUAVE** — total ?; splits: test (-1)

## Metrics

- `SDR improvement` **(primary)** — range: dB
  - Signal-to-Distortion Ratio improvement computed using the BSS Eval toolbox. Measures the quality of separated speech relative to the reference mixture.
- `PESQ` — range: [-2, 4.5]
  - Perceptual Evaluation of Speech Quality. A standard objective metric for speech enhancement quality.
- `STOI` — range: [0, 1]
  - Short-Time Objective Intelligibility. Predicts speech intelligibility based on temporal envelope correlation.

## Input / output format

**Input**: Single-channel audio mixture (speech + noise/other speakers) synchronized with visual face streams (one or more) of the target speaker(s).

**Output**: Separated speech signal(s) or time-frequency masks for each target speaker.

## Scoring recipe

```python
# Compute SDR improvement via BSS Eval
# ref: clean target speech, est: model output, mix: input mixture
sdr_est = bss_eval_sources(ref, est, frame_length=..., hop_length=...)
sdr_mix = bss_eval_sources(ref, mix, frame_length=..., hop_length=...)
sdr_improvement = sdr_est - sdr_mix
return sdr_improvement
```

## Common pitfalls

- Synthetic test sets are generated on-the-fly from AVSpeech and AudioSet with a 90/10 split, meaning there is no fixed public benchmark for direct comparison.
- Real-world video evaluations lack clean reference audio, so they are strictly qualitative and cannot be scored with SDR/PESQ/STOI.
- Prior audio-visual methods are speaker-dependent, while this evaluation uses a speaker-independent model, complicating direct architectural comparisons.

## Evidence (verbatim from paper)

> Separated speech quality is evaluated using signal-to-distortion ratio (SDR) improvement from the BSS Eval toolbox [Vincent et al., 2006], a commonly used metric for evaluating speech separation quality (see Section A in the Appendix).

## Citation

```bibtex
@misc{ephrat2018looking,
  title={Looking to Listen at the Cocktail Party: A Speaker-Independent Audio-Visual Model for Speech Separation},
  author={Ephrat et al. (2018)},
  year={2018},
  note={arXiv:1804.03619}
}
```

- arXiv: 1804.03619

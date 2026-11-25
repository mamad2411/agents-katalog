---
name: audiocaps-sep-eval
description: Evaluates zero-shot language-queried audio source separation using natural language captions rather than fixed labels. The benchmark tests the model's ability to separate a target sound described by human-annotated captions from a mixed audio mixture. Use when the user wants to benchmark on AudioCaps, or asks about evaluating this task. Reports SDRi.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2308.05037
  bibtex_key: liu2023separate
  confidence: high
---

# audiocaps-sep-eval

> Separate Anything You Describe — Liu et al. (2023) (arXiv:2308.05037, 2023)

## What this evaluates

Evaluates zero-shot language-queried audio source separation using natural language captions rather than fixed labels. The benchmark tests the model's ability to separate a target sound described by human-annotated captions from a mixed audio mixture.

## Datasets

- **AudioCaps** — total 4785; splits: test (4785)

## Metrics

- `SDRi` **(primary)** — range: dB
  - Signal-to-distortion ratio improvement, calculated as the difference between the SDR of the separated output and the original mixture.
- `SI-SDR` — range: dB
  - Scale-invariant signal-to-distortion ratio, evaluates separation quality independent of amplitude scaling between prediction and target.

## Input / output format

**Input**: A 10-second audio mixture (SNR 0 dB) containing a target sound and background source, paired with one of five human-annotated natural language captions for the target.

**Output**: Separated audio waveform corresponding to the target sound described by the caption.

## Scoring recipe

```python
def score(pred, gold, mixture):
  sdr_out = compute_sdr(pred, gold)
  sdr_mix = compute_sdr(mixture, gold)
  sdri = sdr_out - sdr_mix
  si_sdr = compute_si_sdr(pred, gold)
  return sdri, si_sdr
```

## Common pitfalls

- Each test audio is mixed with five randomly chosen background sources, creating 5 variations per original clip.
- Background sources are selected such that their sound event tags do not coincide with the target source's tags.

## Evidence (verbatim from paper)

> Our downloaded test set of the AudioCaps dataset includes 957 audio clips, each annotated with five captions. ... Consequently, 4785 test mixtures are created. ... We utilize signal-to-distortion ratio improvement (SDRi) and scale-invariant SDR (SI-SDR) to evaluate the performance of sound separation systems.

## Citation

```bibtex
@misc{liu2023separate,
  title={Separate Anything You Describe},
  author={Liu et al. (2023)},
  year={2023},
  note={arXiv:2308.05037}
}
```

- arXiv: 2308.05037

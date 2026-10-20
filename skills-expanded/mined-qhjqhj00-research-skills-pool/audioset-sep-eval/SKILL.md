---
name: audioset-sep-eval
description: Evaluates zero-shot language-queried audio source separation on a diverse set of environmental and acoustic sound classes. The benchmark tests the model's ability to isolate a target sound described by a text label from a synthetically mixed audio mixture. Use when the user wants to benchmark on AudioSet, or asks about evaluating this task. Reports SDRi.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2308.05037
  bibtex_key: liu2023separate
  confidence: high
---

# audioset-sep-eval

> Separate Anything You Describe — Liu et al. (2023) (arXiv:2308.05037, 2023)

## What this evaluates

Evaluates zero-shot language-queried audio source separation on a diverse set of environmental and acoustic sound classes. The benchmark tests the model's ability to isolate a target sound described by a text label from a synthetically mixed audio mixture.

## Datasets

- **AudioSet** — total 5270; splits: test (5270)

## Metrics

- `SDRi` **(primary)** — range: dB
  - Signal-to-distortion ratio improvement, calculated as the difference between the SDR of the separated output and the original mixture.
- `SI-SDR` — range: dB
  - Scale-invariant signal-to-distortion ratio, evaluates separation quality independent of amplitude scaling between prediction and target.

## Input / output format

**Input**: A 10-second audio mixture (SNR 0 dB) containing two distinct sound classes, paired with a text label query specifying the target sound class.

**Output**: Separated audio waveform corresponding to the target sound class specified by the text query.

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

- Mixtures are synthetically generated at 0 dB SNR using anchor segments from a sound event detection system, not real-world recordings.
- The evaluation uses hierarchical text labels from the AudioSet ontology, not natural language captions.

## Evidence (verbatim from paper)

> The evaluation set of AudioSet contains 20,317 audio clips with 527 sound classes. ... We generate 10 mixtures for each sound class, leading to 5270 mixtures for all 527 sound classes in total. ... We utilize signal-to-distortion ratio improvement (SDRi) and scale-invariant SDR (SI-SDR) to evaluate the performance of sound separation systems.

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

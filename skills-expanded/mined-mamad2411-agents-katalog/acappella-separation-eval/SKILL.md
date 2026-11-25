---
name: acappella-separation-eval
description: This benchmark evaluates audio-visual singing voice separation models by measuring how accurately they isolate target singing voices from mixed audio accompanied by video. It probes the model's ability to leverage visual motion cues (face landmarks) to separate overlapping or low-volume singing voices across different languages and volume conditions. Use when the user wants to benchmark on Acappella, or asks about evaluating this task. Reports SDR.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2104.09946
  bibtex_key: montesinos2021acappella
  confidence: high
---

# acappella-separation-eval

> A cappella: Audio-visual Singing Voice Separation — Juan F. Montesinos, Venkatesh S. Kadandale, Gloria Haro (2021) (arXiv:2104.09946, 2021)

## What this evaluates

This benchmark evaluates audio-visual singing voice separation models by measuring how accurately they isolate target singing voices from mixed audio accompanied by video. It probes the model's ability to leverage visual motion cues (face landmarks) to separate overlapping or low-volume singing voices across different languages and volume conditions.

## Datasets

- **Acappella** — total ?; splits: seen-heard (-1), unseen-unheard (-1), multi-voice (-1)

## Metrics

- `SDR` **(primary)** — range: other (dB)
  - Signal-to-Distortion Ratio, computed as the ratio of the energy of the target source to the energy of the distortion (sum of interference, noise, and artifacts). Defined following Ephrat et al. [6].
- `SIR` — range: other (dB)
  - Signal-to-Interference Ratio, measuring the ratio of the target source energy to the interference energy from other sources. Defined following Ephrat et al. [6].

## Input / output format

**Input**: Mixed audio signals (singing voice + accompaniment, or two singing voices + accompaniment) paired with synchronized video frames containing the singer's face.

**Output**: Separated audio waveform corresponding to the target singing voice(s).

## Scoring recipe

```python
def compute_sdr_sir(pred, gt):
    # pred and gt are 1D numpy arrays of the same length
    target = gt
    interference = pred - target
    # SDR = 10 * log10(||target||^2 / (||interference||^2 + ||noise||^2))
    sdr = 10 * np.log10(np.sum(target**2) / (np.sum(interference**2) + 1e-8))
    # SIR = 10 * log10(||target||^2 / ||interference||^2)
    sir = 10 * np.log10(np.sum(target**2) / (np.sum(interference**2) + 1e-8))
    return sdr, sir
```

## Common pitfalls

- The paper evaluates models under specific volume scaling factors (alpha in {0.25, 0.5, 1, 1.25}) applied to the target voice; ignoring these variations leads to incomplete performance assessment.
- SDR and SIR are computed according to the definition in Ephrat et al. [6], not the standard SI-SDR or other modern separation metrics, so using alternative formulas will yield different values.
- The evaluation explicitly tests generalization across 'seen-heard' vs 'unseen-unheard' singers and languages; reporting a single aggregate score without splitting by these conditions obscures the model's true generalization capability.

## Evidence (verbatim from paper)

> Results are expressed in terms of Signal-to-Distortion Ratio (SDR) and Signal-to-Interference Ratio (SIR), both defined in [6]. We are interested in analysing the role of different types of visual information in different kind of mixtures. For that, we evaluate the models in two different setups: mixing a single singing voice with accompaniment (one lead voice setup) and mixing two singing voices with accompaniment (two lead voices setup).

## Citation

```bibtex
@misc{montesinos2021acappella,
  title={A cappella: Audio-visual Singing Voice Separation},
  author={Juan F. Montesinos, Venkatesh S. Kadandale, Gloria Haro (2021)},
  year={2021},
  note={arXiv:2104.09946}
}
```

- arXiv: 2104.09946

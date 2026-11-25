---
name: audio-spoof-detection-eval
description: Evaluates the robustness of audio spoof detection models against real-world audio degradation and manipulation attacks (laundering), including reverberation, additive noise, and re-compression. Use when the user wants to benchmark on ASVspoof 2019 LA, ASVspoof Laundered Database, or asks about evaluating this task. Reports EER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2408.14712
  bibtex_key: ali2024audiospoof
  confidence: high
---

# audio-spoof-detection-eval

> Is Audio Spoof Detection Robust to Laundering Attacks? — Hashim Ali et al. (arXiv:2408.14712, 2024)

## What this evaluates

Evaluates the robustness of audio spoof detection models against real-world audio degradation and manipulation attacks (laundering), including reverberation, additive noise, and re-compression.

## Datasets

- **ASVspoof 2019 LA** — total ?; splits: train (-1), development (-1), eval (-1)
- **ASVspoof Laundered Database** — total ?; splits: test (-1)

## Metrics

- `EER` **(primary)** — range: percent
  - EER is the operating point where the miss rate ($P_{miss}$) and false alarm rate ($P_{fa}$) are equal.

## Input / output format

**Input**: Audio utterances (bonafide or spoof)

**Output**: Binary classification decision or spoof confidence score

## Scoring recipe

```python
def compute_eer(predictions, labels):
    thresholds = np.linspace(0, 1, 1000)
    miss_rates, fa_rates = [], []
    for t in thresholds:
        pred = (predictions >= t).astype(int)
        miss_rates.append(np.mean(pred[labels == 0]))
        fa_rates.append(np.mean(pred[labels == 1]))
    eer = np.interp(0.5, [(m + f) / 2 for m, f in zip(miss_rates, fa_rates)], [0, 1])
    return eer
```

## Common pitfalls

- Training models on laundered/corrupted data instead of clean ASVspoof 2019 LA train data
- Using min-tDCF without the required false alarm and miss cost parameters
- Aggregating results across all laundering attacks without reporting per-attack degradation

## Evidence (verbatim from paper)

> Following the ASVspoof challenge evaluation plans, the equal error rate (EER) is used as an objective evaluation metric in our experiments [25]. We omit the tandem detection cost function (mint-DCF) as it requires the false alarm and miss costs of the ASV system, which are only available for ASVspoof 2019 eval database. EER corresponds to a CM operating point at which miss rate $(P_{miss})$ and False alarm rate $(P_{fa})$ becomes equal.

## Citation

```bibtex
@misc{ali2024audiospoof,
  title={Is Audio Spoof Detection Robust to Laundering Attacks?},
  author={Hashim Ali et al.},
  year={2024},
  note={arXiv:2408.14712}
}
```

- arXiv: 2408.14712

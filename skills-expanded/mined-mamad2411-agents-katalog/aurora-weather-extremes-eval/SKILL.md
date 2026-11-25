---
name: aurora-weather-extremes-eval
description: Evaluates the predictability and forecast skill of the Aurora AI weather model across selected extreme weather events, including tropical cyclones, winter freezes, and heatwaves. It probes the model's ability to maintain deterministic track accuracy, temperature amplitude, and spatial pattern fidelity across short-range (1–7 day) to subseasonal (14–21 day) lead times. Use when the user wants to benchmark on Selected Weather Extremes Case Studies, or asks about evaluating this task. Reports Track error.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.06516
  bibtex_key: huang2026aurora
  confidence: high
---

# aurora-weather-extremes-eval

> Evaluating the Predictability of Selected Weather Extremes with Aurora, an AI Weather Forecast Model — Huang et al. (2026) (arXiv:2603.06516, 2026)

## What this evaluates

Evaluates the predictability and forecast skill of the Aurora AI weather model across selected extreme weather events, including tropical cyclones, winter freezes, and heatwaves. It probes the model's ability to maintain deterministic track accuracy, temperature amplitude, and spatial pattern fidelity across short-range (1–7 day) to subseasonal (14–21 day) lead times.

## Datasets

- **Selected Weather Extremes Case Studies** — total ?; splits: test (-1); repo https://github.com/microsoft/aurora

## Metrics

- `Track error` **(primary)** — range: km
  - Mean great-circle distance between forecast and best-track position.
- `T2m RMSE` — range: °C
  - Root mean square error of 2-meter temperature forecasts against reanalysis or best-track.
- `Pattern Correlation` — range: [0, 1]
  - Spatial Pearson correlation coefficient between forecast and observed temperature fields.
- `IoU` — range: [0, 1]
  - Intersection over Union of binary masks for extreme events (threshold 0°C for freezes).

## Input / output format

**Input**: Initial atmospheric state fields (ERA5 reanalysis) at initialization time (00/06/12/18 UTC) to generate deterministic forecasts.

**Output**: Forecasted atmospheric fields (TC track coordinates, 2-meter temperature grids) at specified lead times (1, 3, 5, 7, 14, 21 days).

## Scoring recipe

```python
# TC Track Error
track_err = mean(great_circle_dist(pred_track, gold_track))
# T2m RMSE & Bias
rmse = sqrt(mean((pred_t2m - gold_t2m)**2))
bias = mean(pred_t2m - gold_t2m)
# Pattern Correlation
corr = pearsonr(pred_t2m.flatten(), gold_t2m.flatten())
# IoU (0°C threshold)
pred_mask = (pred_t2m <= 0)
gold_mask = (gold_t2m <= 0)
iou = sum(pred_mask & gold_mask) / sum(pred_mask | gold_mask)
```

## Common pitfalls

- Long-lead skill degradation is driven by amplitude collapse rather than loss of large-scale circulation patterns, which can be misleading if only pattern correlation is reported.
- Intensity errors (MSLP, 10m winds) are highly sensitive to the decoder/diagnostic method and small structural errors, requiring cautious interpretation.
- Direct comparisons with operational NWP systems were not performed; results rely on climatological error ranges from official sources (e.g., NHC) rather than paired forecasts.

## Evidence (verbatim from paper)

> At 1-day lead, both events show strong spatial skill (Table 5). For Beast from the East, pattern correlation reaches 0.994, spatial extent is 68.5%, and IoU is 0.979, indicating near-complete overlap of the freeze footprint. RMSE is 7.03°C with a minimal warm bias of +0.19°C.

## Citation

```bibtex
@misc{huang2026aurora,
  title={Evaluating the Predictability of Selected Weather Extremes with Aurora, an AI Weather Forecast Model},
  author={Huang et al. (2026)},
  year={2026},
  note={arXiv:2603.06516}
}
```

- arXiv: 2603.06516

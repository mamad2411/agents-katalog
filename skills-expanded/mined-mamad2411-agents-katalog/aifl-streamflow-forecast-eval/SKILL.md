---
name: aifl-streamflow-forecast-eval
description: Evaluates a model's ability to forecast daily specific streamflow at global gauging stations under temporal generalization. It specifically probes robustness to domain shifts between reanalysis pre-training data and operational forecast fine-tuning data, testing whether the model maintains performance when transitioning from historical reanalysis to real-time operational forcing. Use when the user wants to benchmark on CARAVAN v1.5, or asks about evaluating this task. Reports KGE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.16579
  bibtex_key: taccari2026aifl
  confidence: high
---

# aifl-streamflow-forecast-eval

> AIFL: A Global Daily Streamflow Forecasting Model Using Deterministic LSTM Pre-trained on ERA5-Land and Fine-tuned on IFS — Taccari et al. (2026) (arXiv:2602.16579, 2026)

## What this evaluates

Evaluates a model's ability to forecast daily specific streamflow at global gauging stations under temporal generalization. It specifically probes robustness to domain shifts between reanalysis pre-training data and operational forecast fine-tuning data, testing whether the model maintains performance when transitioning from historical reanalysis to real-time operational forcing.

## Datasets

- **CARAVAN v1.5** — total 18588; splits: train (-1), val (-1), test (2003)

## Metrics

- `KGE` **(primary)** — range: [-1, 1]
  - Kling-Gupta Efficiency: $1 - \sqrt{(r-1)^2 + (\alpha-1)^2 + (\beta-1)^2}$, where $r$ is Pearson correlation, $\alpha$ is ratio of standard deviations, and $\beta$ is ratio of means.
- `NSE` — range: [-1, 1]
  - Nash-Sutcliffe Efficiency: $1 - \frac{\sum(Q_{obs}-Q_{sim})^2}{\sum(Q_{obs}-\bar{Q}_{obs})^2}$, measuring relative magnitude of residual variance compared to observed variance.

## Input / output format

**Input**: Daily time series of 5 meteorological variables (SSR, STR, SP, T2M, TP) over a 170-day hindcast window, concatenated with 203 static catchment attributes, seasonal sine/cosine encodings, and UTC offset.

**Output**: 10-day forecast of daily specific discharge (mm/d) per station.

## Scoring recipe

```python
def compute_kge(obs, sim):
    r = pearsonr(obs, sim)
    alpha = std(sim) / std(obs)
    beta = mean(sim) / mean(obs)
    return 1 - sqrt((r-1)**2 + (alpha-1)**2 + (beta-1)**2)

def compute_nse(obs, sim):
    return 1 - sum((obs - sim)**2) / sum((obs - mean(obs))**2)

# Aggregate across 2003 test basins
kge_scores = [compute_kge(obs_i, sim_i) for i in range(2003)]
nse_scores = [compute_nse(obs_i, sim_i) for i in range(2003)]
median_kge = median(kge_scores)
median_nse = median(nse_scores)
```

## Common pitfalls

- Spatial overlap between basins causes severe data leakage if not strictly deduplicated (KGE≥0.95 threshold used for removal).
- Temporal split (2021–2024) is used instead of spatial split due to gauge availability, biasing evaluation toward larger catchments.
- Domain shift between ERA5-Land reanalysis and IFS operational forecasts degrades performance if not mitigated via two-stage training.

## Evidence (verbatim from paper)

> This approach mitigates performance degradation due to differing error structures between training and operational forcing data, achieving median KGE' of 0.66 and NSE of 0.53 on an independent test set (2021–2024), outperforming traditional process-based models in ungauged basins while maintaining computational efficiency and operational transparency.

## Citation

```bibtex
@misc{taccari2026aifl,
  title={AIFL: A Global Daily Streamflow Forecasting Model Using Deterministic LSTM Pre-trained on ERA5-Land and Fine-tuned on IFS},
  author={Taccari et al. (2026)},
  year={2026},
  note={arXiv:2602.16579}
}
```

- arXiv: 2602.16579

---
name: air-quality-forecasting-eval
description: Evaluates a regression model's ability to forecast hyper-local air pollutant concentrations using fine-grained traffic intensity descriptors. It probes how well traffic patterns across different spatial rings and colors correlate with specific pollutant levels under varying training station configurations. Use when the user wants to benchmark on Mexico City Traffic & Pollution Dataset, or asks about evaluating this task. Reports RMSE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.23215
  bibtex_key: bona2026sapiens
  confidence: high
---

# air-quality-forecasting-eval

> Tackling air quality with SAPIENS — Bona et al. (2026) (arXiv:2601.23215, 2026)

## What this evaluates

Evaluates a regression model's ability to forecast hyper-local air pollutant concentrations using fine-grained traffic intensity descriptors. It probes how well traffic patterns across different spatial rings and colors correlate with specific pollutant levels under varying training station configurations.

## Datasets

- **Mexico City Traffic & Pollution Dataset** — total ?; splits: train (-1), val (-1)

## Metrics

- `RMSE` **(primary)** — range: other
  - Root Mean Squared Error: sqrt(1/N * sum((y_i - y_hat_i)^2)), where y_i are true pollutant concentrations and y_hat_i are predicted values. Used to select the number of PLSR components via cross-validation and to compare training scenarios.

## Input / output format

**Input**: 60-dimensional vector of traffic intensity descriptors (15 concentric rings × 4 color categories) per observation.

**Output**: 9-dimensional vector of predicted pollutant concentrations (e.g., PM2.5, PM10, O3, CO, NOx, SO2).

## Scoring recipe

```python
def compute_rmse(predictions, targets):
    # predictions and targets are arrays of shape (N, 9)
    squared_errors = (predictions - targets) ** 2
    mean_squared_error = np.mean(squared_errors, axis=0)
    rmse = np.sqrt(mean_squared_error)
    return rmse.mean()
```

## Common pitfalls

- The PLSR model optimizes linear combinations of all 9 pollutants simultaneously rather than predicting each pollutant independently, which compresses the prediction range for low-correlation pollutants.
- The number of PLSR components (n_comp) is fixed via cross-validation to minimize RMSE, which acts as a capacity constraint and must be reported per scenario (7, 4, or 9).
- Station similarity is evaluated using a weighted chi-square score based on VIP weights, but the primary forecasting performance is measured strictly by RMSE.

## Evidence (verbatim from paper)

> In our analysis, the PLSR was trained to predict the nine pollutant measurements from the 60 traffic intensities, hence we used p=60 traffic predictors and m=9 pollutant response variables from eq.[2]. We define a benchmark model as the model that was trained and tested on the data from three stations (CAM, MER and TLA). We then validated this model using station PED. ... The overall Root Mean Squared Errors (RMSE) is lowest when six stations are used for training as shown in Fig.[13], while it is higher for the single SAG station training pointing at the benefit of more data over station similarity.

## Citation

```bibtex
@misc{bona2026sapiens,
  title={Tackling air quality with SAPIENS},
  author={Bona et al. (2026)},
  year={2026},
  note={arXiv:2601.23215}
}
```

- arXiv: 2601.23215

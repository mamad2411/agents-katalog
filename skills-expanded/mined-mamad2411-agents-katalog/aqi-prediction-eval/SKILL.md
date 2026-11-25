---
name: aqi-prediction-eval
description: Evaluates machine learning models' ability to predict Air Quality Index (AQI) across Indian cities using historical pollutant concentrations and location metadata. It probes the models' capacity to capture temporal patterns and spatial variations in air pollution, particularly around agricultural burning events. Use when the user wants to benchmark on Indian Air Quality Monitoring Dataset (22 stations), or asks about evaluating this task. Reports R².
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.08702
  bibtex_key: sidhu2024predictive
  confidence: high
---

# aqi-prediction-eval

> Predictive Modelling of Air Quality Index (AQI) Across Diverse Cities and States of India using Machine Learning: Investigating the Influence of Punjab's Stubble Burning on AQI Variability — Sidhu et al. (2024) (arXiv:2404.08702, 2024)

## What this evaluates

Evaluates machine learning models' ability to predict Air Quality Index (AQI) across Indian cities using historical pollutant concentrations and location metadata. It probes the models' capacity to capture temporal patterns and spatial variations in air pollution, particularly around agricultural burning events.

## Datasets

- **Indian Air Quality Monitoring Dataset (22 stations)** — total ?; splits: train (-1), test (-1)

## Metrics

- `R²` **(primary)** — range: [0, 1]
  - Coefficient of determination, measuring the proportion of variance in the dependent variable (AQI) explained by the model. Calculated as 1 - (SS_res / SS_tot).
- `MSE` — range: other
  - Mean Squared Error, the average of the squares of the errors between predicted and actual values.
- `RMSE` — range: other
  - Root Mean Squared Error, the square root of MSE, providing error magnitude in the same units as the target variable.
- `MAE` — range: other
  - Mean Absolute Error, the average absolute difference between predicted and actual values.

## Input / output format

**Input**: Time-stamped records containing 8 pollutant concentrations (PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO) and one-hot encoded categorical features for state and city.

**Output**: Continuous numerical prediction of the Air Quality Index (AQI).

## Scoring recipe

```python
def calculate_metrics(y_true, y_pred):
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(y_true - y_pred))
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R2': r2}
```

## Common pitfalls

- SARIMAX was not trained on the full dataset, making direct performance comparisons with other models invalid.
- Lack of meteorological variables (temperature, humidity, wind direction) limits the model's ability to capture true causal drivers of AQI variability.
- High computational cost for LSTM models may lead to under-tuning or early stopping if resources are constrained.

## Evidence (verbatim from paper)

> For accurately evaluating the performance metrics different statistical measures are used like MSE, RMSE, R2, and MAE. Different prediction models are used to predict AQI so using these metrics can help to monitor the model's performance. The main matrix for the model's performance evaluation especially for regression models is R2. It is clear from figure 21 that the value of R2 is almost 1 for the Random Forest regressor followed by CatBoost and XGBoost ML models.

## Citation

```bibtex
@misc{sidhu2024predictive,
  title={Predictive Modelling of Air Quality Index (AQI) Across Diverse Cities and States of India using Machine Learning: Investigating the Influence of Punjab's Stubble Burning on AQI Variability},
  author={Sidhu et al. (2024)},
  year={2024},
  note={arXiv:2404.08702}
}
```

- arXiv: 2404.08702

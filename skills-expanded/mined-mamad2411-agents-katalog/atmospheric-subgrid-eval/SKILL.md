---
name: atmospheric-subgrid-eval
description: Evaluates neural network parameterizations for predicting subgrid atmospheric processes (e.g., microphysical tendencies, momentum fluxes) using single-column versus non-local (3x3 grid) inputs. It probes the model's ability to capture mesoscale convective dynamics and frontal systems, and assesses performance across different atmospheric stability regimes. Use when the user wants to benchmark on SAM (Simple Atmospheric Model) simulation, or asks about evaluating this task. Reports R^2.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2201.00417
  bibtex_key: wang2022nonlocal
  confidence: high
---

# atmospheric-subgrid-eval

> Non-local parameterization of atmospheric subgrid processes with neural networks — Wang et al. (2022) (arXiv:2201.00417, 2022)

## What this evaluates

Evaluates neural network parameterizations for predicting subgrid atmospheric processes (e.g., microphysical tendencies, momentum fluxes) using single-column versus non-local (3x3 grid) inputs. It probes the model's ability to capture mesoscale convective dynamics and frontal systems, and assesses performance across different atmospheric stability regimes.

## Datasets

- **SAM (Simple Atmospheric Model) simulation** — total ?; splits: test (-1)

## Metrics

- `R^2` **(primary)** — range: [-1, 1]
  - Coefficient of determination calculated globally by concatenating vertical columns for each target variable. Defined as 1 - (sum of squared residuals / total sum of squares).
- `Improvement Index` — range: other
  - Normalized difference in squared errors between a baseline single-column model (NN1D) and a non-local model (NN3D), divided by the climatological variance of the ground truth at a given latitude: ((NN1D - true)^2 - (NN3D - true)^2) / σ_true^2.

## Input / output format

**Input**: Vertical atmospheric columns (single-column or 3x3 grid of neighboring columns) containing state variables such as temperature, water mixing ratios, zonal/meridional winds, and optionally vertical velocity or horizontal wind divergence.

**Output**: Predicted subgrid tendencies and fluxes, specifically: tendency of total precipitating water mixing ratio due to microphysics, subgrid fluxes of non-precipitating mixing ratio, subgrid energy flux, coarse-grained diffusivity, and subgrid zonal/meridional momentum fluxes.

## Scoring recipe

```python
def calculate_r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

def calculate_improvement_index(y_true, y_pred_nn1d, y_pred_nn3d, sigma_true_var):
    err_nn1d = (y_true - y_pred_nn1d) ** 2
    err_nn3d = (y_true - y_pred_nn3d) ** 2
    return (err_nn1d - err_nn3d) / sigma_true_var
```

## Common pitfalls

- Global R^2 values can be overstated because they partly reflect correctly predicting the mean at each vertical level; performance should be verified after removing column means.
- The improvement index is normalized by latitude-dependent climatological variance, so absolute improvements in the tropics may appear smaller than in mid-latitudes due to high tropical variance.
- Including vertical velocity as an input is not equivalent to including horizontal wind divergence, despite their relationship via mass continuity, due to coarse-graining effects on line averages.

## Evidence (verbatim from paper)

> To measure the performance of NN1D, NN3D, NN1D +w and NN1D +δ , we calculate the global R^2 values by concatenating vertical columns for each target variable (Figure 2). ... Next, we want to understand for which atmospheric states NN3D predicts better than NN1D. We first define an improvement index for each individual test sample for each of the output variables and each atmospheric level as: Improvement = ((NN1D - true)^2 - (NN3D - true)^2) / σ_true^2, where (NN1D - true)^2 is the squared error of NN1D output, (NN3D - true)^2 is the squared error of NN3D output, and σ_true^2 is the variance of the ground truth over the column and over all testing samples which is a latitude-dependent variable.

## Citation

```bibtex
@misc{wang2022nonlocal,
  title={Non-local parameterization of atmospheric subgrid processes with neural networks},
  author={Wang et al. (2022)},
  year={2022},
  note={arXiv:2201.00417}
}
```

- arXiv: 2201.00417

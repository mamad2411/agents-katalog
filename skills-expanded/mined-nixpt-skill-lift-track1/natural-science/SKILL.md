---
name: natural-science
description: |
  Scientific computing and natural-science analysis: signal processing,
  astronomy/earth-science pipelines, lab unit harmonization, experiment
  notebooks, and numeric reproducibility. Use for seismic/GW/exoplanet-style
  tasks, unit conversion, JAX/numpy scientific code, and measurement datasets
  — not for pure SWE debugging or office document formatting.
---

# natural-science

Load `safe-agent-scope` before any state-changing action; science pipelines do not waive sandbox, recipient, or injection rules.

## Why

Science tasks fail on **units, coordinates, sampling rates, and
reproducibility** more often than on missing formulas. Make assumptions
explicit and keep numeric pipelines deterministic.

## Procedure

1. **Identify measurables** — quantities, units, frames (time, lat/lon, freq).
2. **Harmonize units** early; fail loudly on missing unit metadata.
3. **Pipeline** — load → clean → transform → estimate → plot/table → save.
4. **Sanity bounds** — physical ranges (e.g. probabilities ∈ [0,1], latitudes).
5. **Reproducibility** — fixed seeds; record library methods used.
6. **Deliver** — write the exact artifact the instruction names; verify with
   `verify-task-output`.

## Heuristics

- Prefer established libraries (numpy/scipy/astropy/obspy-like) over hand-rolled FFTs when available in the environment
- Separate calibration/constants from data tables
- Document coordinate systems when transforming geospatial or sensor data

## Anti-patterns

- Silent unit swaps (m vs km, deg vs rad)
- Overfitting noise with overly complex models when a simple estimator is specified
- Dropping "outlier" points without a rule tied to the instruction

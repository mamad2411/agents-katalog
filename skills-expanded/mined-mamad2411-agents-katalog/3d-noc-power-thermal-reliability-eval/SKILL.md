---
name: 3d-noc-power-thermal-reliability-eval
description: Evaluates a simulation platform for predicting power consumption, thermal distribution, and reliability (MTTF) of 3D Networks-on-Chip under synthetic and application workloads. It compares TSV-based 3D-NoC designs against monolithic and 2D-IC alternatives, and assesses the impact of different floorplans and cooling strategies on thermal stress and failure rates. Use when the user wants to benchmark on PARSEC benchmark suite, Synthetic benchmarks (Matrix, HotSpot, Uniform, Transpose), or asks about evaluating this task. Reports power_consumption.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2003.08648
  bibtex_key: dang2020powerthermalreliability
  confidence: high
---

# 3d-noc-power-thermal-reliability-eval

> Report on power, thermal and reliability prediction for 3D Networks-on-Chip — Dang et al. (2020) (arXiv:2003.08648, 2020)

## What this evaluates

Evaluates a simulation platform for predicting power consumption, thermal distribution, and reliability (MTTF) of 3D Networks-on-Chip under synthetic and application workloads. It compares TSV-based 3D-NoC designs against monolithic and 2D-IC alternatives, and assesses the impact of different floorplans and cooling strategies on thermal stress and failure rates.

## Datasets

- **PARSEC benchmark suite** — total ?; splits: eval (-1)
- **Synthetic benchmarks (Matrix, HotSpot, Uniform, Transpose)** — total ?; splits: eval (-1)

## Metrics

- `power_consumption` **(primary)** — range: other
  - Estimated using router power models scaled by flit counts and routing data, combined with static and dynamic power parameters from NANGATE 45nm library. Calculated as energy per data bit multiplied by total bits processed.
- `temperature` — range: other
  - Simulated using Hotspot 6.0 with modified thermal resistivity for Copper TSVs. Resistivity is computed via parallel combination of TIM and Copper areas.
- `mttf` — range: [0, 1]
  - Mean Time To Failure estimated using Black's model based on simulated temperature and activation energy. Values are normalized to a baseline of 323.15K (50°C) for comparison across layers and benchmarks.

## Input / output format

**Input**: Router floorplan geometry, TSV dimensions and placement, benchmark traces (flit injection rates and routing paths), power scaling equations, and thermal material properties (TIM and Copper resistivity).

**Output**: Numerical values for static/dynamic power (Watts, J/bit), per-layer temperature maps (Kelvin), normalized MTTF ratios per layer/benchmark, and execution time of the prediction pipeline (seconds).

## Scoring recipe

```python
def evaluate_3d_noc(benchmarks, floorplan, tsv_params):
    power_map = estimate_power(benchmarks, router_model, flit_counts)
    R_joint = compute_tsv_resistivity(tsv_params['area'], tsv_params['R_TIM'], tsv_params['R_Copper'])
    temp_map = hotspot_6_0_simulate(power_map, R_joint, floorplan)
    mttf_raw = black_model(temp_map, activation_energy)
    mttf_normalized = mttf_raw / black_model(323.15, activation_energy)
    return power_map, temp_map, mttf_normalized
```

## Common pitfalls

- Using standard TIM or copper thermal resistivity values without applying the paper's specific parallel-area formula for TSV joint resistivity.
- Comparing the simulation flow's execution time directly with physical fabrication-based reliability tests without noting the orders-of-magnitude methodological difference.
- Assuming monolithic 3D-ICs are universally hotter or less reliable; the paper notes they have lower area cost and different thermal density, requiring careful baseline comparison.

## Evidence (verbatim from paper)

> In this section, we use Black's model to evaluate the MTTF of 3D-NoC. Figure 11 and Figure 12 show the normalized MTTF of each layer to 323.15K (50°C) under PARSEC and synthetic benchmarks. Here, we can observe TSV-based 3D-NoC dominates Monolithic in the PARSEC benchmark.

## Citation

```bibtex
@misc{dang2020powerthermalreliability,
  title={Report on power, thermal and reliability prediction for 3D Networks-on-Chip},
  author={Dang et al. (2020)},
  year={2020},
  note={arXiv:2003.08648}
}
```

- arXiv: 2003.08648

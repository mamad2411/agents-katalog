---
name: agentcaster-tornado-forecasting-eval
description: Evaluates multimodal LLMs' ability to perform spatiotemporal reasoning and probabilistic risk forecasting for tornadoes by interactively querying weather data and generating geographic risk polygons. It measures forecasting accuracy, hallucination severity, and geometric precision against official meteorological baselines. Use when the user wants to benchmark on TornadoBench, or asks about evaluating this task. Reports TornadoBench.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.03349
  bibtex_key: chen2025agentcaster
  confidence: high
---

# agentcaster-tornado-forecasting-eval

> AgentCaster: Reasoning-Guided Tornado Forecasting — Chen (2025) (arXiv:2510.03349, 2025)

## What this evaluates

Evaluates multimodal LLMs' ability to perform spatiotemporal reasoning and probabilistic risk forecasting for tornadoes by interactively querying weather data and generating geographic risk polygons. It measures forecasting accuracy, hallucination severity, and geometric precision against official meteorological baselines.

## Datasets

- **TornadoBench** — total ?; splits: test (-1); repo https://github.com/agentcaster/agentcaster

## Metrics

- `TornadoBench` **(primary)** — range: percent
  - Composite percentage score measuring primary forecasting accuracy of predicted risk polygons against ground truth tornado reports. Higher values indicate better alignment with official forecasts.
- `TornadoHallucination` — range: [0, 1]
  - Measures hallucination frequency and severity, split into Simple and Hard variants. Lower values indicate fewer or less severe hallucinations or geographic misplacements.
- `Max Risk Match` — range: percent
  - Percentage of days where the model's maximum predicted risk level falls Under, Match, or Over the ground truth maximum risk.

## Input / output format

**Input**: High-resolution spatiotemporal weather data accessed via interactive tools, combined with a system prompt defining the AI meteorologist role, forecasting objective, and tool usage constraints.

**Output**: GeoJSON format specifying probabilistic risk polygons for tornado forecasting.

## Scoring recipe

```python
def compute_tornado_bench(pred_geojson, gt_reports):
    # Calculate overlap/accuracy between predicted risk polygons and ground truth
    # Returns a percentage score (0-100) where higher is better
    return percentage_score

def compute_tornado_hallucination(pred_geojson, gt_reports, variant):
    # Quantify frequency and severity of hallucinations or geographic misplacements
    # Simple vs Hard variants penalize different levels of error
    # Returns a score in [0, 1] where lower is better
    return hallucination_score
```

## Common pitfalls

- Many models fail to generate syntactically valid GeoJSON outputs, causing prediction drops.
- Increased reasoning steps do not improve performance; some models show monotonic degradation in TornadoBench scores with more complex reasoning.
- Centroid distance errors often exceed 400–500 km, revealing poor geographic precision even when outputs are valid.

## Evidence (verbatim from paper)

> The primary forecasting accuracy, hallucination metrics, and maximum risk matching for the LLM configurations and the SPC baseline are presented in Table [2]. Agent interaction statistics and centroid distance errors are detailed in Table [3] (centroid computation described in Appendix[C]). The SPC baseline achieves a TornadoBench score of 18.31%, significantly outperforming all evaluated LLM agents.

## Citation

```bibtex
@misc{chen2025agentcaster,
  title={AgentCaster: Reasoning-Guided Tornado Forecasting},
  author={Chen (2025)},
  year={2025},
  note={arXiv:2510.03349}
}
```

- arXiv: 2510.03349

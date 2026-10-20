---
name: ai-quality
description: Evaluates a feature-hierarchical edge inference framework's ability to dynamically allocate communication and computation resources to maximize AI quality under strict latency and energy constraints. Use when the user has predictions and gold and needs to compute AI quality (mAP).
metadata:
  skill_kind: metric
  source_arxiv: 2211.07860
  bibtex_key: choi2022enabling
  confidence: medium
---

# ai-quality

> Enabling AI Quality Control via Feature Hierarchical Edge Inference — Choi et al. (2022) (arXiv:2211.07860, 2022)

## What this evaluates

Evaluates a feature-hierarchical edge inference framework's ability to dynamically allocate communication and computation resources to maximize AI quality under strict latency and energy constraints.

## Datasets

- **YOLO v3 (unspecified dataset)** — total ?; splits: test (-1)

## Metrics

- `AI quality (mAP)` **(primary)** — range: [0, 1]
  - Mean Average Precision (mAP) scaled by a feature size coefficient (δ_s = 12 mAP/Mbyte). The optimization objective maximizes the sum of AI quality across all mobiles.

## Input / output format

**Input**: Raw input data (100 Kbytes), channel state information, and per-mobile computation/energy/latency constraints.

**Output**: Optimized uplink/downlink bandwidth allocation, edge/mobile computation FLOPS allocation, and selected feature scale, yielding a final AI quality score.

## Scoring recipe

```python
# Pseudo-code for the optimization objective

total_ai_quality = 0
for mobile in mobiles:
    feature_size = select_feature_scale(mobile.channel_state)
    ai_quality[mobile] = feature_size * delta_s  # delta_s = 12 mAP/Mbyte
    total_ai_quality += ai_quality[mobile]

# Constraints: avg_energy <= 5 J, avg_latency <= 15 sec
# Return allocation that maximizes total_ai_quality
```

## Common pitfalls

- The paper uses simulation parameters rather than a standard benchmark dataset; YOLO v3 is mentioned but the underlying dataset is not specified.
- AI quality is a composite metric derived from mAP and feature size, not a direct classification accuracy score.
- Benchmarks compare against simplified resource allocation strategies (constant quality, computation-only optimization) rather than modern edge inference frameworks.

## Evidence (verbatim from paper)

> We consider two benchmarks: constant AI quality and FHEI with computation resource optimization only. For the first benchmark, every mobile’s AI quality is fixed but optimized under the same constraints as the proposed FHEI... δ_s | Coefficient of quality function | 12 mAP/Mbyte

## Citation

```bibtex
@misc{choi2022enabling,
  title={Enabling AI Quality Control via Feature Hierarchical Edge Inference},
  author={Choi et al. (2022)},
  year={2022},
  note={arXiv:2211.07860}
}
```

- arXiv: 2211.07860

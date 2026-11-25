---
name: average_frame_timing
description: This benchmark evaluates the real-time rendering performance of a VR NeRF system by measuring the time required to generate each frame under varying field-of-view (FoV) and pixel-per-degree (PPD) settings. It probes the system's ability to maintain interactive framerates (≥30 FPS) while fusing neural radiance fields with CAD geometry in immersive virtual reality. Use when the user has predictions and gold and needs to compute average frame timing.
metadata:
  skill_kind: metric
  source_arxiv: 2307.09860
  bibtex_key: li2023magicnerflens
  confidence: high
---

# average_frame_timing

> Magic NeRF Lens: Interactive Fusion of Neural Radiance Fields for Virtual Facility Inspection — Ke Li et al. (2023) (arXiv:2307.09860, 2023)

## What this evaluates

This benchmark evaluates the real-time rendering performance of a VR NeRF system by measuring the time required to generate each frame under varying field-of-view (FoV) and pixel-per-degree (PPD) settings. It probes the system's ability to maintain interactive framerates (≥30 FPS) while fusing neural radiance fields with CAD geometry in immersive virtual reality.

## Datasets

- **EuXFEL particle accelerator section** — total 60; splits: (unstated); repo https://github.com/uhhhci/immersive-ngp

## Metrics

- `average frame timing` **(primary)** — range: other
  - Mean rendering time per frame (in milliseconds) over a specified 3D camera trajectory. Real-time VR performance is defined as < 33.33 ms (≥30 FPS).

## Input / output format

**Input**: Pre-recorded or user-followed 3D camera trajectory, NeRF model, CAD model context, and rendering parameters (FoV, PPD, DLSS settings).

**Output**: Rendered stereoscopic frames and logged per-frame timing values.

## Scoring recipe

```python
frame_times = []
for frame in trajectory:
    render_time = system.render(frame, fov, ppd, context)
    frame_times.append(render_time)
avg_frame_time = sum(frame_times) / len(frame_times)
is_realtime = avg_frame_time < 33.33
```

## Common pitfalls

- Confusing Field of View (FoV) with Pixel Per Degree (PPD) when interpreting performance scaling trends.
- Failing to account for HMD driver overhead, which adds 5-10 ms to live benchmarks compared to replay benchmarks.
- Assuming DLSS is disabled by default, though the paper explicitly states it is critical and enabled for all benchmarks.

## Evidence (verbatim from paper)

> we collected the average frame timing ($\overline{f_{t}}$) for stereoscopic rendering of different display FoV and PPD configurations by replaying the same pre-recorded 3D trace. ... As expected, the rendering latency scales linearly with increasing FoV for the basic NeRF lens effect. Additionally, it is shown that our system could theoretically achieve real-time VR rendering of 30 frames per second ($\overline{f_{t}}<33.33ms$) at less than $50^{\circ}$ FoV.

## Citation

```bibtex
@misc{li2023magicnerflens,
  title={Magic NeRF Lens: Interactive Fusion of Neural Radiance Fields for Virtual Facility Inspection},
  author={Ke Li et al. (2023)},
  year={2023},
  note={arXiv:2307.09860}
}
```

- arXiv: 2307.09860

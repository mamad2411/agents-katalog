---
name: cfg-zero-star-guidance
description: Classifier-Free Guidance with CFG-Zero-Star negative-prompt projection scaling for flow-matching diffusion
category: diffusion
version: 1.0.0
tags: [diffusion, cfg, flow-matching, guidance, audio]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/OpenBMB/VoxCPM.git
source_ref: main
source_commit: 13605c5a0e6b99d6d3527a43bd1a4e0e69c8800e
source_project: VoxCPM
source_paths:
  - src/voxcpm/modules/locdit/unified_cfm.py
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
---

# Classifier-Free Guidance with CFG-Zero-Star negative-prompt scaling

## When to use
Use this pattern in flow-matching or score-based diffusion models where you want stronger adherence to the conditional signal without the typical CFG artifacts (over-saturation, clipping) that appear at high guidance scales. CFG-Zero-Star re-projects the negative (unconditional) prediction to remove its component parallel to the positive prediction, giving a cleaner direction vector.

Also supports `sway_sampling_coef` for trajectory adjustment at no additional network cost.

## Pattern

### Standard CFG (reference)
```python
# Standard CFG (for comparison)
def cfg_standard(pos, neg, cfg_value):
    return neg + cfg_value * (pos - neg)
```

### CFG-Zero-Star variant
```python
import torch

def cfg_zero_star(pos: torch.Tensor, neg: torch.Tensor, cfg_value: float) -> torch.Tensor:
    """
    CFG-Zero-Star: re-scale negative by its projection onto positive
    before computing the guidance direction.

    pos: conditional model output   [B, T, D]
    neg: unconditional model output [B, T, D]
    cfg_value: guidance scale (1.0 = no guidance, 2-3 = typical)
    """
    # Compute scalar projection of neg onto pos direction
    # st_star = (pos · neg) / ||neg||²
    dot = (pos * neg).sum(dim=-1, keepdim=True)          # [B, T, 1]
    neg_norm_sq = (neg * neg).sum(dim=-1, keepdim=True)  # [B, T, 1]
    st_star = dot / (neg_norm_sq + 1e-8)                 # [B, T, 1]

    # Guidance direction uses the re-scaled negative
    return pos + cfg_value * st_star * (pos - neg)
```

### Combining with sway sampling
Sway sampling adjusts the timestep trajectory before the network call, independent of the guidance formula:

```python
import math

def sway_sample_timesteps(t_span: torch.Tensor, coef: float = 1.0) -> torch.Tensor:
    """
    Adjust ODE timestep schedule with a cosine perturbation.
    coef=1.0 is neutral; 0.8 pushes timesteps earlier, 1.2 later.
    """
    return t_span + coef * (torch.cos(math.pi / 2 * t_span) - 1 + t_span)

def sample_step(model, x, t, cond, uncond, cfg_value, use_cfg_zero_star, sway_coef):
    t_adj = sway_sample_timesteps(t, sway_coef)
    pos = model(x, t_adj, cond)
    neg = model(x, t_adj, uncond)
    if use_cfg_zero_star:
        return cfg_zero_star(pos, neg, cfg_value)
    else:
        return cfg_standard(pos, neg, cfg_value)
```

### Wiring into the sampling loop
```python
# In unified_cfm.py pattern
for t in timesteps:
    velocity = sample_step(
        model=dit,
        x=x_t,
        t=t,
        cond=cond_feat,
        uncond=uncond_feat,
        cfg_value=2.0,
        use_cfg_zero_star=True,
        sway_coef=1.0,
    )
    x_t = x_t + velocity * dt
```

## Source reference
- Upstream: `OpenBMB/VoxCPM` @ `main` / `13605c5a`
- Key files:
  - `src/voxcpm/modules/locdit/unified_cfm.py:23-130` — full CFM sampler with CFG-Zero-Star and sway sampling

## Notes
- CFG-Zero-Star is most beneficial at `cfg_value >= 2.5`; below that, standard CFG and Zero-Star produce nearly identical results.
- The `1e-8` epsilon in the denominator prevents division by zero when the unconditional prediction is near zero (which can happen early in denoising).
- `sway_sampling_coef` and `use_cfg_zero_star` are independent knobs — you can use either without the other.

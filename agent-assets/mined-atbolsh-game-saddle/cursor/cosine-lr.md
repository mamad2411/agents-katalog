---
description: Cosine LR must match the run length and stay at the floor past it
alwaysApply: true
---

# Cosine learning rate — match the run, then stay down

When you set up a trainer, the cosine horizon is the run's optimizer-step
budget. Compute it from the stop condition. A leftover from a shorter run,
or a steps-per-second placeholder, is the wrong horizon: the LR hits the
floor early and the rest of the run never decays.

- **Images.** Steps = images × (optimizer steps per image from the refill
  arithmetic). On resume, horizon = restored step + remaining images × that
  rate. The same curve, not a new cosine started at step 0.
- **Hours only.** There is no image count to multiply. Require an explicit
  horizon. Do not invent one from a constant steps/second.
- **Past the horizon the multiplier is the floor.** An unclamped
  `0.5 * (1 + cos(pi * progress))` turns around and climbs back to the peak
  once progress passes 1. PyTorch `CosineAnnealingLR` does the same thing
  past `T_max`. Clamp: `if step >= total: return floor`.

```python
# BAD — climbs after total, and 140_000 was a different run
return 0.5 * (1 + math.cos(math.pi * step / total))

# GOOD — floor holds, horizon is this run
if step >= total:
    return floor
```

---
name: aimbot-calc
description: Calculate optimal input angles. Trigger: aimbot, aim angle, smooth aim, fov check, target prediction.
tool: Python math
x-alice-class: game
---# aimbot-calc

## Trigger
`aimbot, aim angle, smooth aim, fov check, target prediction`

## Flow
```
read positions -> calc_angle() -> smooth_aim() -> fov_check() -> output module
```

## Script
`scripts/aimbot_calc.py`

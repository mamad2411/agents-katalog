---
name: world-to-screen
description: 3D world to 2D screen projection. Trigger: world to screen, projection, screen coordinates, w2s math.
tool: Python math
x-alice-class: game
---# world-to-screen

## Trigger
`world to screen, projection, screen coordinates, w2s math`

## Flow
```
read view matrix -> w2s(pos, matrix, w, h) -> (x, y)
```

## Script
`scripts/world_to_screen.py`

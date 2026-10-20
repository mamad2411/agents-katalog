---
name: overlay-render
description: Transparent overlay rendering via DirectX. Trigger: overlay, transparent window, directx, d2d, render overlay.
tool: Python + ctypes + Direct2D
x-alice-class: game
---# overlay-render

## Trigger
`overlay, transparent window, directx, d2d, render overlay`

## Flow
```
CreateWindowEx(WS_EX_TOPMOST|TRANSPARENT) -> D2D init -> draw loop -> output full overlay.py
```

## Script
`scripts/overlay_render.py`

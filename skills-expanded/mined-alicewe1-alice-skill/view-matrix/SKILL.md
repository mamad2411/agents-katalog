---
name: view-matrix
description: Locate view projection matrix. Trigger: view matrix, projection, camera matrix, world to screen, w2s.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Cheat Engine\Cheat Engine.exe
x-alice-class: game
---# view-matrix

## Trigger
`view matrix, projection, camera matrix, world to screen, w2s`

## Flow
```
CE search angles -> 16 floats in [-1,1] -> output matrix address + w2s code
```

## Script
`scripts/view_matrix.py`

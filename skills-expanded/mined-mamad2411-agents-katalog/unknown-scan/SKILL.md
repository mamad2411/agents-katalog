---
name: unknown-scan
description: Scan memory for unknown/changing values. Trigger: unknown value, fuzzy scan, changed, increased, decreased.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Cheat Engine\Cheat Engine.exe
x-alice-class: game
---# unknown-scan

## Trigger
`unknown value, fuzzy scan, changed, increased, decreased`

## Flow
```
CE -> Unknown initial -> filter changes -> output matched addresses
```

## Script
`scripts/unknown_scan.py`

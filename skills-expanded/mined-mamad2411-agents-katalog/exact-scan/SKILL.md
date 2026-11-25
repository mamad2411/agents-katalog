---
name: exact-scan
description: Scan process memory for known values. Trigger: scan, search value, find address, exact value, gold, health, ammo.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Cheat Engine\Cheat Engine.exe
x-alice-class: game
---# exact-scan

## Trigger
`scan, search value, find address, exact value, gold, health, ammo`

## Flow
```
CE attach -> First Scan -> change value -> Next Scan -> output addresses + lock script
```

## Script
`scripts/exact_scan.py`

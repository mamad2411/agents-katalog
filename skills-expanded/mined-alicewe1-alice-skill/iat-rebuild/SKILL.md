---
name: iat-rebuild
description: Rebuild import address table. Trigger: iat, import table, rebuild, fix imports, invalid pointer.
tool: Scylla (x64dbg plugin)
x-alice-class: reverse
---# iat-rebuild

## Trigger
`iat, import table, rebuild, fix imports, invalid pointer`

## Flow
```
Scylla -> IAT Autosearch -> Get Imports -> Fix Dump -> verify
```

## Script
`scripts/iat_rebuild.py`

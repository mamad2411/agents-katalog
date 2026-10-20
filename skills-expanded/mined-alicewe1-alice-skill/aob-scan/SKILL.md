---
name: aob-scan
description: Array of bytes pattern scan. Trigger: aob, array of bytes, pattern scan, signature, byte pattern.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\game_hacker.py
x-alice-class: reverse
---# aob-scan

## Trigger
`aob, array of bytes, pattern scan, signature, byte pattern`

## Flow
```
find unique bytes around target -> output AOB pattern + scan script
```

## Script
`scripts/aob_scan.py`

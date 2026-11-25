---
name: time-reset
description: Remove time/trial limitations. Trigger: time bomb, trial, expire, date check, timer, trial reset.
tool: x64dbg + registry
x-alice-class: crack
---# time-reset

## Trigger
`time bomb, trial, expire, date check, timer, trial reset`

## Flow
```
break on GetSystemTime -> hook to return fixed date -> or registry/file trial reset
```

## Script
`scripts/time_reset.py`

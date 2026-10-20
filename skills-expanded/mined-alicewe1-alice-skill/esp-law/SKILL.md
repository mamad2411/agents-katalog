---
name: esp-law
description: ESP-based original entry point location. Trigger: esp law, pushad, popad, entry point, oep, original entry.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\x64dbg\release\x64\x64dbg.exe
x-alice-class: reverse
---# esp-law

## Trigger
`esp law, pushad, popad, entry point, oep, original entry`

## Flow
```
x64dbg -> F8 -> HW BP on ESP -> F9 -> popad -> far jump -> OEP -> dump
```

## Script
`scripts/esp_law.py`

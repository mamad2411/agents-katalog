---
name: memory-breakpoint
description: Memory breakpoint OEP method. Trigger: memory breakpoint, text section, code section, section bp.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\x64dbg\release\x64\x64dbg.exe
x-alice-class: reverse
---# memory-breakpoint

## Trigger
`memory breakpoint, text section, code section, section bp`

## Flow
```
x64dbg -> Memory Map -> .text section -> memory access BP -> F9 -> OEP -> dump
```

## Script
`scripts/memory_breakpoint.py`

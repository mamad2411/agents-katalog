---
name: nop-remove
description: Remove instructions with NOP fill. Trigger: nop, remove instruction, disable check, skip call, bypass validation.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\software_cracker.py
x-alice-class: reverse
---# nop-remove

## Trigger
`nop, remove instruction, disable check, skip call, bypass validation`

## Flow
```
identify target instructions -> output offset+count -> write 0x90
```

## Script
`scripts/nop_remove.py`

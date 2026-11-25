---
name: jmp-modify
description: Modify conditional jumps to unconditional. Trigger: jmp patch, unconditional jump, je to jmp, jne to nop.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\software_cracker.py
x-alice-class: reverse
---# jmp-modify

## Trigger
`jmp patch, unconditional jump, je to jmp, jne to nop`

## Flow
```
x64dbg read opcode -> output patch bytes -> software_cracker.py apply
```

## Script
`scripts/jmp_modify.py`

---
name: jump-patch
description: Modify conditional flow at decision points. Trigger: jump, je, jne, jmp, nop, patch jump, conditional.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\software_cracker.py
x-alice-class: reverse
---# jump-patch

## Trigger
`jump, je, jne, jmp, nop, patch jump, conditional`

## Flow
```
x64dbg locate decision -> output patch bytes -> software_cracker.py apply
```

## Script
`scripts/jump_patch.py`

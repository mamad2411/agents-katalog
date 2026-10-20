---
name: code-inject
description: Inject custom code into process. Trigger: inject, code cave, auto assemble, hook code, dll load.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Cheat Engine\Cheat Engine.exe
x-alice-class: reverse
---# code-inject

## Trigger
`inject, code cave, auto assemble, hook code, dll load`

## Flow
```
CE Auto Assembler -> alloc+write+jmp -> output [ENABLE]...[DISABLE] script
```

## Script
`scripts/code_inject.py`

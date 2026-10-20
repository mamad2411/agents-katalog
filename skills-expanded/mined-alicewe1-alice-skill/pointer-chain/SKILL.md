---
name: pointer-chain
description: Find stable multi-level pointer chains. Trigger: pointer, offset, base address, static address, dynamic address.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\Tool\Cheat Engine\Cheat Engine.exe
x-alice-class: game
---# pointer-chain

## Trigger
`pointer, offset, base address, static address, dynamic address`

## Flow
```
CE find value -> Pointer Scan -> restart -> Rescan -> output [[base+off1]+off2]
```

## Script
`scripts/pointer_chain.py`

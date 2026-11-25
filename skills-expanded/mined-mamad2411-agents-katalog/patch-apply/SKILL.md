---
name: patch-apply
description: Apply byte patches to binary. Trigger: apply patch, write bytes, modify binary, overwrite, hex patch.
tool: C:\Users\Administrator\Desktop\ai2\新破甲\scripts\software_cracker.py
x-alice-class: reverse
---# patch-apply

## Trigger
`apply patch, write bytes, modify binary, overwrite, hex patch`

## Flow
```
software_cracker.py patch --target --offset --original --patched -> verify
```

## Script
`scripts/patch_apply.py`
